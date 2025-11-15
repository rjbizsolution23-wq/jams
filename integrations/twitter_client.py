"""
Twitter API Client for JAMS
Handles automated posting to Twitter/X
"""

import os
import tweepy
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TwitterClient:
    """Twitter API client for automated posting"""
    
    def __init__(self):
        self.consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self.consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        if not all([self.consumer_key, self.consumer_secret, 
                   self.access_token, self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials")
        
        # Initialize OAuth 1.0a client (for posting)
        self.auth = tweepy.OAuth1UserHandler(
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        
        # Initialize OAuth 2.0 client (for reading)
        if self.bearer_token:
            self.client_v2 = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
    
    def post_tweet(
        self,
        text: str,
        media_ids: Optional[list] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post a tweet
        
        Args:
            text: Tweet text (max 280 characters)
            media_ids: List of media IDs to attach
            reply_to: Tweet ID to reply to
            
        Returns:
            Dict with tweet data
        """
        try:
            if len(text) > 280:
                text = text[:277] + "..."
            
            kwargs = {}
            if media_ids:
                kwargs['media_ids'] = media_ids
            if reply_to:
                kwargs['in_reply_to_status_id'] = reply_to
            
            tweet = self.api.update_status(status=text, **kwargs)
            
            logger.info(f"Tweet posted successfully: {tweet.id}")
            
            return {
                "success": True,
                "tweet_id": tweet.id_str,
                "text": tweet.text,
                "created_at": tweet.created_at.isoformat(),
                "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
            }
        except tweepy.TweepyException as e:
            logger.error(f"Failed to post tweet: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_media(self, file_path: str) -> Optional[str]:
        """
        Upload media file to Twitter
        
        Args:
            file_path: Path to media file
            
        Returns:
            Media ID string or None
        """
        try:
            media = self.api.media_upload(file_path)
            logger.info(f"Media uploaded: {media.media_id_string}")
            return media.media_id_string
        except tweepy.TweepyException as e:
            logger.error(f"Failed to upload media: {e}")
            return None
    
    def post_product(
        self,
        product_name: str,
        product_description: str,
        price: float,
        product_url: str,
        image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post a product announcement tweet
        
        Args:
            product_name: Product name
            product_description: Product description
            price: Product price
            product_url: URL to product page
            image_url: Optional product image URL
            
        Returns:
            Dict with tweet data
        """
        # Format tweet text
        tweet_text = f"🔥 New Content Pack Available!\n\n{product_name}\n\n"
        
        # Truncate description if needed
        max_desc_length = 200 - len(tweet_text) - len(product_url) - 20
        if len(product_description) > max_desc_length:
            description = product_description[:max_desc_length] + "..."
        else:
            description = product_description
        
        tweet_text += f"{description}\n\n💰 ${price:.2f}\n\n🔗 {product_url}\n\n#NSFW #AdultContent #FetishVerse"
        
        # Upload image if provided
        media_ids = None
        if image_url:
            # Download image temporarily
            import requests
            import tempfile
            
            try:
                response = requests.get(image_url)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    tmp.write(response.content)
                    media_id = self.upload_media(tmp.name)
                    if media_id:
                        media_ids = [media_id]
                    os.unlink(tmp.name)
            except Exception as e:
                logger.warning(f"Failed to upload product image: {e}")
        
        return self.post_tweet(tweet_text, media_ids=media_ids)
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information"""
        try:
            user = self.api.verify_credentials()
            return {
                "id": user.id_str,
                "username": user.screen_name,
                "name": user.name,
                "followers_count": user.followers_count,
                "friends_count": user.friends_count
            }
        except tweepy.TweepyException as e:
            logger.error(f"Failed to get user info: {e}")
            return {"error": str(e)}


# Singleton instance
_twitter_client: Optional[TwitterClient] = None


def get_twitter_client() -> TwitterClient:
    """Get or create Twitter client instance"""
    global _twitter_client
    if _twitter_client is None:
        _twitter_client = TwitterClient()
    return _twitter_client

