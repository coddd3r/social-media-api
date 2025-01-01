

** TEST IN  VIRTUALENV **


 BE Capstone Project: Social Media API
Project Overview:

As a backend developer, your task is to design and implement a Social Media API using Django and Django REST Framework. This API will allow users to create, update, delete posts, follow other users, and view a feed of posts from the users they follow. You will be responsible for managing user data, posts, and interactions between users in a simulated real-world social media environment. The project will give you experience in user relationships, database interactions, and handling large datasets, all while focusing on CRUD operations and API design.
Functional Requirements:

    Post Management (CRUD):
        Implement the ability to Create, Read, Update, and Delete (CRUD) posts.
        Each post should have the following attributes: Content (text), User (author), Timestamp, and optional Media (e.g., image URLs).
        Ensure validation for required fields like Content and User.
        Users can only update or delete their own posts.

    Users Management (CRUD):
        Implement CRUD operations for users.
        Each user should have a unique Username, Email, Password, and a profile that includes optional fields like Bio and Profile Picture.
        Only authenticated users should be able to create, update, or delete their own posts.

    Follow System:
        Create an endpoint to allow users to follow and unfollow other users.
        Implement a system to store the follower and following relationships between users.
        Ensure that users cannot follow themselves.

    Feed of Posts:
        Create an endpoint to allow users to view a feed of posts from the users they follow.
            The feed should display posts in reverse chronological order (most recent posts first).
            Optionally, allow users to filter the feed by date or search for posts by keyword.

** TEST IN  VIRTUALENV **
Technical Requirements:

    Database:
        Use Django ORM to interact with the database.
        Define models for Users, Posts, and Followers.
        Ensure that each post is linked to a user and followers/following relationships are tracked efficiently.

    Authentication:
        Implement user authentication using Django’s built-in authentication system.
        Users must be logged in to create, update, or delete posts, follow other users, or view their feed.
        Optionally, implement token-based authentication (JWT) to provide secure access to the API.

    API Design:
        Use Django Rest Framework (DRF) to design and expose the necessary API endpoints.
        Follow RESTful principles, using appropriate HTTP methods (GET, POST, PUT, DELETE) for different operations.
        Ensure proper error handling, with relevant HTTP status codes (e.g., 404 for not found, 400 for bad request).

    Deployment:
        Deploy the API on Heroku or PythonAnywhere.
        Ensure that the API is accessible, secure, and performs well in the deployed environment.

    Pagination and Sorting:
        Add pagination to the feed of posts for users with large numbers of followed users or a large volume of posts.
        Provide sorting options such as sorting by Date or Popularity (likes, comments).

** TEST IN  VIRTUALENV **
Stretch Goals (Optional):

    Likes and Comments: Implement the ability for users to like and comment on posts, with endpoints to manage likes and comments.
    Notifications: Add a notification system where users are notified when someone follows them, likes their post, or comments on it.
    Direct Messaging: Implement a direct messaging feature allowing users to send private messages to each other.
    Post Sharing and Reposts: Add functionality for users to share or “repost” content from other users in their feed.
    Hashtags and Tagging: Allow users to tag other users in posts or use hashtags, with endpoints to view posts tagged with specific hashtags or mentions.
    Trending Posts: Implement a feature to display trending posts based on the number of likes or reposts in a given period.
    Profile Customization: Allow users to customize their profile with additional fields such as Location, Website, and Cover Photo.
    Media Uploads: Add functionality for users to upload media files (images, videos) with their posts, storing these files on a cloud service like AWS S3.
