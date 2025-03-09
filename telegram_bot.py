import os
import logging
import traceback
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from datetime import datetime
from app import db, Candidate, app
from advanced_resume_parser import AdvancedResumeParser
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

load_dotenv()

# Get bot token and list of allowed users
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USERNAMES = os.getenv('ALLOWED_TELEGRAM_USERNAMES', '').split(',')
RESUME_FOLDER = 'resumes'

# Create resume folder if it doesn't exist
if not os.path.exists(RESUME_FOLDER):
    os.makedirs(RESUME_FOLDER)

parser = AdvancedResumeParser()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends welcome message."""
    user = update.message.from_user
    logger.info(f"User {user.username} ({user.id}) started the bot")
    await update.message.reply_text(
        'Hello! I am a resume processing bot with advanced data recognition. '
        'Send me a resume file (PDF or DOC/DOCX), and I will analyze it.'
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles received documents."""
    user = update.message.from_user
    logger.info(f"Document received from user {user.username} ({user.id})")
    
    # Check if user has access
    if user.username not in ALLOWED_USERNAMES:
        logger.warning(f"Access denied to user {user.username}")
        await update.message.reply_text(
            'Sorry, you do not have access to this bot. '
            'Please contact the administrator for access.'
        )
        return

    document = update.message.document
    if not document:
        logger.warning("No document found in message")
        return

    # Check file extension
    file_name = document.file_name.lower()
    logger.info(f"Received file: {file_name}")
    
    if not file_name.endswith(('.pdf', '.doc', '.docx')):
        logger.warning(f"Unsupported file format: {file_name}")
        await update.message.reply_text(
            'Please send the resume in PDF, DOC, or DOCX format.'
        )
        return

    try:
        # Create unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{timestamp}_{document.file_name}"
        file_path = os.path.join(RESUME_FOLDER, new_filename)
        logger.info(f"Saving file as: {file_path}")

        # Download file
        logger.debug("Starting file download")
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(file_path)
        logger.info("File successfully downloaded")

        # Determine resume sender
        original_sender = None
        if update.message.forward_from:
            original_sender = update.message.forward_from
            logger.info(f"Resume forwarded from user: {original_sender.username}")
        elif update.message.forward_sender_name:
            original_sender_name = update.message.forward_sender_name
            logger.info(f"Resume forwarded from user with hidden profile: {original_sender_name}")

        # Parse resume
        logger.debug("Starting resume parsing")
        resume_data = parser.parse_resume(file_path)
        logger.info(f"Parsing result: {resume_data}")

        if resume_data:
            # Work with database in application context
            with app.app_context():
                # Check if candidate with this email already exists
                existing_candidate = Candidate.query.filter_by(email=resume_data['email']).first()
                
                if existing_candidate:
                    # Update existing record
                    existing_candidate.name = resume_data['name']
                    existing_candidate.phone = resume_data['phone']
                    existing_candidate.resume_path = file_path
                    existing_candidate.specializations = ','.join(resume_data['specializations'])
                    existing_candidate.telegram_username = original_sender.username if original_sender else (
                        update.message.forward_sender_name if update.message.forward_sender_name else user.username
                    )
                    existing_candidate.updated_at = datetime.utcnow()
                    db.session.commit()
                    candidate = existing_candidate
                else:
                    # Create new record
                    candidate = Candidate(
                        name=resume_data['name'],
                        email=resume_data['email'],
                        phone=resume_data['phone'],
                        resume_path=file_path,
                        status='Check',
                        specializations=','.join(resume_data['specializations']),
                        telegram_username=original_sender.username if original_sender else (
                            update.message.forward_sender_name if update.message.forward_sender_name else user.username
                        )
                    )
                    db.session.add(candidate)
                    db.session.commit()
            
            # Send results message
            message = f"✅ Resume successfully processed!\n\n"
            message += f"👤 Name: {resume_data['name']}\n"
            message += f"📧 Email: {resume_data['email']}\n"
            message += f"📱 Phone: {resume_data['phone']}\n"
            message += f"💼 Specializations: {', '.join(resume_data['specializations'])}\n"
            if original_sender:
                message += f"👤 Sender: @{original_sender.username}"
            
            await update.message.reply_text(message)
        else:
            logger.warning("Failed to extract data from resume")
            await update.message.reply_text(
                "⚠️ Failed to extract data from resume. "
                "File saved but requires manual processing."
            )

    except Exception as e:
        logger.error(f"Error processing resume: {traceback.format_exc()}")
        await update.message.reply_text("❌ An error occurred while processing the resume. Please try again later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends help message."""
    user = update.message.from_user
    logger.info(f"User {user.username} requested help")
    await update.message.reply_text(
        'Send me a resume file in PDF, DOC, or DOCX format, '
        'and I will automatically analyze it.\n\n'
        'Supported formats:\n'
        '- PDF\n'
        '- DOC/DOCX\n\n'
        'I will automatically determine:\n'
        '- Candidate name (using NLP)\n'
        '- Email\n'
        '- Phone\n'
        '- Specialization (using AI)\n\n'
        'You can also forward resumes from other users, '
        'and I will save information about the original sender.'
    )

def main():
    """Starts the bot."""
    logger.info("Starting bot")
    logger.info(f"Allowed users: {ALLOWED_USERNAMES}")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start bot
    logger.info("Bot is running and ready to work")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 