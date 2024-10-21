import json
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("Client attempting to connect")
        await self.accept()
        logger.info("Client connection accepted")
        
        # Send initial connection success message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected successfully'
        }))
        
        # Start the stock data stream
        await self.start_stock_stream()
    
    async def disconnect(self, close_code):
        logger.info(f"Client disconnected with code: {close_code}")
        self.is_connected = False
    
    async def start_stock_stream(self):
        self.is_connected = True
        
        while self.is_connected:
            try:
                # Generate some sample data instead of connecting to external WebSocket
                sample_data = [
                    {
                        'symbol': 'AAPL',
                        'price': 150.25,
                        'volume': 1000,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        'symbol': 'GOOGL',
                        'price': 2800.75,
                        'volume': 500,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        'symbol': 'MSFT',
                        'price': 290.50,
                        'volume': 750,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
                
                # Send the sample data
                await self.send(text_data=json.dumps({
                    'type': 'stock_update',
                    'data': sample_data
                }))
                
                # Wait for 2 seconds before sending next update
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error in stock stream: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying
                continue