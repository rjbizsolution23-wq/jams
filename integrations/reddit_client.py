"""
Reddit API Client for JAMS
Handles automated posting to Reddit
"""

import os
import praw
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class RedditClient:
    """Reddit API client for automated posting"""
    
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "JAMS/1.0 by rjbizsolution23-wq")
        self.username = os.getenv("REDDIT_USERNAME")
        self.password = os.getenv("REDDIT_PASSWORD")
        
        if not all([self.client_id, self.client_secret, 
                   self.username, self.password]):
            raise ValueError("Missing Reddit API credentials")
        
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            username=self.username,
            password=self.password
        )
        
        # Verify authentication
        try:
            self.reddit.user.me()
            logger.info(f"Reddit authenticated as: {self.reddit.user.me()}")
        except Exception as e:
            logger.error(f"Reddit authentication failed: {e}")
            raise
    
    def post_to_subreddit(
        self,
        subreddit_name: str,
        title: str,
        text: Optional[str] = None,
        url: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post to a subreddit
        
        Args:
            subreddit_name: Name of subreddit (without r/)
            title: Post title
            text: Post text (for self posts)
            url: URL to link (for link posts)
            image_path: Path to image file (for image posts)
            
        Returns:
            Dict with post data
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Determine post type
            if image_path:
                submission = subreddit.submit_image(
                    title=title,
                    image_path=image_path
                )
            elif url:
                submission = subreddit.submit(
                    title=title,
                    url=url
                )
            elif text:
                submission = subreddit.submit(
                    title=title,
                    selftext=text
                )
            else:
                raise ValueError("Must provide text, url, or image_path")
            
            logger.info(f"Posted to r/{subreddit_name}: {submission.id}")
            
            return {
                "success": True,
                "post_id": submission.id,
                "title": submission.title,
                "url": f"https://reddit.com{submission.permalink}",
                "subreddit": subreddit_name,
                "created_at": submission.created_utc
            }
        except praw.exceptions.PRAWException as e:
            logger.error(f"Failed to post to Reddit: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def post_product(
        self,
        product_name: str,
        product_description: str,
        price: float,
        product_url: str,
        category: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post a product announcement to appropriate subreddit
        
        Args:
            product_name: Product name
            product_description: Product description
            price: Product price
            product_url: URL to product page
            category: Product category (for subreddit selection)
            image_url: Optional product image URL
            
        Returns:
            Dict with post data
        """
        # Map categories to subreddits
        subreddit_map = {
            "foot-fetish": "FootFetish",
            "bdsm": "BDSMcommunity",
            "latex": "LatexLovers",
            "cosplay": "NSFWcosplay",
            "anime": "animeNSFW",
            "milf": "milf",
            "ebony": "Ebony",
            "asian": "AsianNSFW"
        }
        
        subreddit_name = subreddit_map.get(category, "NSFW")
        
        # Format post
        title = f"{product_name} - Premium Content Pack"
        text = f"{product_description}\n\n💰 Price: ${price:.2f}\n🔗 [Get it here]({product_url})\n\n#NSFW #AdultContent"
        
        # Download image if provided
        image_path = None
        if image_url:
            import requests
            import tempfile
            
            try:
                response = requests.get(image_url)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    tmp.write(response.content)
                    image_path = tmp.name
            except Exception as e:
                logger.warning(f"Failed to download product image: {e}")
        
        result = self.post_to_subreddit(
            subreddit_name=subreddit_name,
            title=title,
            text=text if not image_path else None,
            image_path=image_path
        )
        
        # Clean up temp file
        if image_path and os.path.exists(image_path):
            try:
                os.unlink(image_path)
            except:
                pass
        
        return result
    
    def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """Get information about a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return {
                "name": subreddit.display_name,
                "subscribers": subreddit.subscribers,
                "description": subreddit.public_description,
                "over18": subreddit.over18
            }
        except praw.exceptions.PRAWException as e:
            logger.error(f"Failed to get subreddit info: {e}")
            return {"error": str(e)}


# Singleton instance
_reddit_client: Optional[RedditClient] = None


def get_reddit_client() -> RedditClient:
    """Get or create Reddit client instance"""
    global _reddit_client
    if _reddit_client is None:
        _reddit_client = RedditClient()
    return _reddit_client

