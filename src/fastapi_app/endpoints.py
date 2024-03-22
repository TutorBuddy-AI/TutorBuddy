from src.admin.newsletter_admin.newsletter_admin import Newsletter
from src.fastapi_app import app

import traceback


@app.get('/start_newsletter/datetime')
async def send_newsletter():
    try:
        await Newsletter().send_newsletter()
        return {'message': 'Newsletter sent'}
    except Exception as e:
        traceback.print_exc()


