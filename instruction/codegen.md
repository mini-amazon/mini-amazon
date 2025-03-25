You are an AI code generator responsible for implementing a web application based on a provided technical specification and implementation plan.

Your task is to systematically implement the implementation plan.

First, carefully review the following inputs:

<project_request>
Standard Course Project: Mini-Amazon
See the overall Course Project Overview (available from the Schedule section of the course website) for general information and important dates. This document is specific to the standard project option.
Overview
In this project, you will build a miniature version of Amazon. On this website, sellers can create product listings and an inventory of products for sale. Users can browse and purchase products. Transactions are conducted within the website using virtual currency. Users can review products and sellers who fulfill their orders.

This project is designed to help you divide work among a team of 5. Each of you will be responsible for implementing a subset of the functionalities described further below:
Users Guru: responsible for Account / Purchases
Products Guru: responsible for Products
Carts Guru: responsible for Cart / Order
Sellers Guru: responsible for Inventory / Order Fulfillment
Social Guru: responsible for Feedback / Messaging
That said, you cannot work in isolation: you will need to collaborate closely on the overall database and website designs, and on integrating and testing your code together.
Functionalities
Account / Purchases
Basic requirements:
A new user can register for a new account; an existing user can log in using email and password.
Each user account has a system-assigned id. Other account information includes email, full name of user, address, and password. Users can update all information except the id. Ensure that email is unique among all users.
Each account is associated with a balance. It starts out as $0, but can be topped up by the user. The user can also withdraw up to the full balance. In practice these actions would require some real payment mechanism, but it is not required for this project.
Users can browse their history of purchases, sorted in reverse chronological order by default. For each purchase in this list, show a summary (e.g., total amount, number of items, and fulfillment status) and link to the detailed order page (see Cart / Order).
Provide a public view for a user. It will show the account number and name as well as any other summary information you deem necessary. If the user also acts as a seller, show also email, address, and include a section with all reviews for this seller (see Feedback / Messaging).
Possible additional features:
Search/filter purchase history by item, by seller, by date etc.
Visualize history of balances, spending amounts and purchases by category, etc.
Products
Basic requirements:
There is a list of predefined product categories, and each product belongs to one category. At the minimum, a product should have a short name, a longer description, an image, and a price.
Users can browse and search/filter all products. For each product in the result list, show a summary (e.g., image, name, average review rating, etc.) and link to the detailed product page. At the minimum, support browsing by category, searching by keywords in name/description, and sorting by price.
A detailed product page will show all details for the product, together with a list of sellers and their current quantities in stock. For each seller, provide an interface for adding a specific quantity of the product from this seller to the user’s cart (see Cart / Order). The page should also include a section showing all reviews for this product (see Feedback / Messaging).
Users can create new products for sale. The user who created a product will be able to edit the product information.
Possible additional features:
There are many more enhancements you can make to filtering/sorting a list of products: e.g., sorting by average review rating or total sales, filtering by rating, price, and/or availability of highly rated sellers, etc.
A flat list of top-level product categories is constraining. Consider a hierarchy of labels, or in general a set of “tags” for labeling products. What is the process for creating and maintaining these labels?
For the same product, different users in our system may create their own versions of this product in our system. Is there a process for “standardizing” products across sellers, and should we allow different sellers to charge different prices?
Cart / Order
Basic requirements:
Each user has a cart. The detailed product page (see Products) will provide a way of adding to this cart. Each line item in the cart refers to one product from one seller with a specific quantity. A detailed cart page should list all line items (quantities and unit prices) and the total price. It should also provide ways to change quantities, remove line items, and submit the entire cart as an order.
When submitting the order, make sure to check available inventories and balances. Beware that inventories and prices can be constantly changing. For simplicity of this project, we will update inventories and balances at the time of order submission. The buyer’s balance will be decremented, and the sellers’ balances will be incremented and inventories decremented. Once the order is placed, the cart becomes empty.
The cart contents are persistent: i.e., they should remain after users leave the site and log back in.
A detailed order page (from the buyer’s perspective) should contain all the information that would have been found on the cart page, but with prices “final.” In addition, for each line item, it should show if and when that line item has been fulfilled by the seller (see Inventory / Order Fulfillment).
The entire order should be marked as fulfilled if all line items are fulfilled. Once submitted, an order cannot be changed by the buyer.
Possible additional features:
Divide the cart into “in cart” and “saved for later” so that a user can check out certain items while keeping the others saved to be purchased at a later time. Items can then be added back into the cart.
Implement promotional coupon codes for certain items, allowing a user to enter some code to get a discount on either a single item, a group of items, or their entire cart.
Inventory / Order Fulfillment
Basic requirements:
A user who wishes to act as a seller will have an inventory page that lists all products for sale by this user. There should be a way to add a product to the inventory. For each product in the user’s inventory, the user can view and change the available quantity for sale by this user, or simply remove it altogether from the inventory.
A seller can browse/search the history of orders fulfilled or to be fulfilled, sorted by in reverse chronological order by default. For each order in this list, show a summary (buyer information including address, date order placed, total amount/number of items, and overall fulfillment status), but do not show information concerning other sellers (recall that an order may involve multiple sellers), and provide a mechanism for marking a line item as fulfilled. (Recall from Cart / Order that order submission automatically decrements the available quantity in the seller’s inventory; so fulfillment should not further update the inventory.)
Possible additional features:
Add visualization/analytics to the inventory and/or order fulfillment pages to show popularity and trends of one’s products.
Add analytics about buyers who have worked with this seller, e.g., ratings, number of messages, etc.
Feedback / Messaging
Basic requirements:
A user can submit a single rating/review for a product. The submission link will be incorporated in the detailed product page (see Products). The user cannot submit multiple ratings/reviews for the same product, but can edit/remove any existing ratings/reviews by this user.
A user can submit a single rating/review for a seller, provided that the user has ordered something from the seller. Incorporate the submission link in appropriate places in the website, e.g., the detailed order page (see Cart / Order) and the public view of a seller (see Account / Purchases). Again, the user cannot submit multiple ratings/reviews for the same seller, but an existing rating/review can be edited or removed.
Each user should be able to list all ratings/reviews authored by this user, sorted in reverse chronological order by default. From this interface the user should be able then select ratings/reviews to update. Incorporate the link to this interface in user account view (see Account / Purchases).
Produce summary ratings for products and sellers; pages or sections showing lists of reviews for products and sellers. At the very least, the summary needs include the average and number of ratings; the reviews lists should be sorted by rating or date.
Possible additional features:
For an order placed by a user, and for any seller fulfilling this order, the user can start a message thread. This message thread is private to the user and the given seller. Messages should be listed in chronological order, and old messages cannot be edited or deleted. Links to these message threads will be shown in buyers’ and sellers’ views of orders.
Upvote functionality for rating/reviews to allow certain reviews to be marked as more or less helpful. By default the top 3 most helpful reviews would be shown first, and then the most recent following these.
Include the ability to submit a limited number of images in the reviews, and make these easily available to users on the website.
Putting Them Together
Basic requirements:
Make sure all functionalities described above under different parts are put together into coherent designs, for both frontend and backend. The website needs to support smooth user task flows across clicks and seamless transitions between different parts. 
Possible additional features:
Develop some methods for recommending products based on past purchase history (both a user’s personal history and the history across all users) as well as reviews. The recommendations can be shown in a “You may also like...” section when a user is looking at products, the current cart contents, or even the purchase history.
In reality, orders don’t get fulfilled instantaneously. Design a process by which sellers can indicate when items have been shipped and buyers can verify when items have been received, as well as protocol for resolving issues (i.e., when orders are not fulfilled by a reasonable deadline, when they are returned, or when there are disputes). You might want to rethink when balances are actually updated in your system.
Getting Started & Getting Help
using Python, Django, and PostgreSQL 

The course website also provides a separate Django tutorial under its Help section, with an example website built on the familiar beer drinkers’ database (although it was coded in a slightly different style using an object-relational mapping framework).

Duke OIT/CoLab offers a wealth of relevant Roots courses/tutorials/workshops that you might find useful to this project.
What to Submit
Milestone 1
README.txt: list your team members, state that you choose the standard project option, and pick a short, catchy name for your team.
Milestone 2
At this point, your team is expected to have set up your own project repo; everyone should have gotten the skeleton code to run in their own development environment and successfully completed the tutorial; and finally, you have collectively come up with an overall design for your database and website.

README.txt: list your team members and their roles (see Overview), briefly summarize what each of you have done since the last milestone, and include a link to your GitLab/GitHub repo.
REPORT.pdf: showing:
Your database design. A diagram would be helpful but is not required. List and describe all tables, constraints, and any assumptions you are additionally making or deviating from our standard assumptions.
A preliminary page-by-page design of your website, as well as how users interact with different parts. We are not expecting any fancy website mock-ups, just the content descriptions and logical flow/connections among pages.
Milestone 3
At this point, each of you should have completed the implementation of at least one backend API endpoint involving executing SQL, as well as the corresponding frontend elements for displaying results and interacting with backend API endpoints. The endpoint you implement will depend on which guru you are working as:
Users Guru: Given a user id, find all purchases of that user.
Products Guru: Given an integer k, find the top k most expensive products.
Carts Guru: Given a user id, find the items in the cart for that user.
Sellers Guru: Given id of a merchant/seller, find the products that are in their inventory.
Social Guru: Given a user id, find the 5 most recent feedback they posted.

You also need to prepare a short demo video (< 3 minutes) of your entire project team demonstrating the working functionality of all APIs and frontend elements above, end to end. You can have one member controlling the app the entire time, but the person who coded each endpoint should be providing the voiceover. For each member, a demo may look something like the following (as an example):
Type something into some textbox, press a button;
Show and interact with the results;
Type something else into the textbox, and rinse and repeat…

Submit the following:
README.txt: as before, plus:
A link to your short video.
Where to find in your code the implementation of the required items above.
CODE.zip: all your code.

Note on zipping for submission: You may crash Gradescope if you submit a big zip file with too many files. Therefore, when zipping directly from your working directory, try excluding unnecessary files, such as those in the hidden .venv directory. Or, submit the zip file that you download from your Git repository, which should exclude these files by default.
Milestone 4
At this point, you should be well under way towards completing your project. In particular, you should have successfully integrated some different pieces that you and your teammates have worked on separately previously. Finally, you should also create a much larger database that can be used for more comprehensive testing and final demo. The database should be large enough to show how you cope with data at scale, e.g., pagination for lists with lots of contents. Instead of creating the contents by hand, you can write a data generator or scraper.

You also need to prepare a second video (< 5 minutes) demonstrating a working (though perhaps not complete) prototype involving both frontend and backend components.

Submit the following:
README.txt: as before, plus:
A link to your short video.
Where to find in your code the implementation of required items above.
Each of you may optionally indicate whether you prefer to be individually scored on the final product (by default, you will not be individually scored). Your preference will be respected, except when the majority of the team prefers individual scoring, every member of the team will be individually scored.
Note that this is your last chance to indicate your preference. This deadline is intended to give everybody a chance to adapt. After this point, complaints of the form “my teammates did nothing” will not be considered.
REPORT.pdf: as before, plus:
A refined database design, highlighting what has changed since the last submitted design.
An updated design for your website. Highlight what has changed since the last milestone. Again, focus on contents/flow instead of presentation.
A list of advanced features that you have implemented or plan to implement and the proposed bonus points for each of these.
CODE.zip: all your code.
Final Report and Demo Video
For the final submission, prepare a video about ~10-15 minutes in length that demonstrates all functionalities of your website. We recommend the following flow for your video:
Browsing as a guest (unauthenticated user)
Should succeed: browse product details; search products; rank and filter
Should fail: all sell/buy/comment actions; checkout
Flexible: add product to cart
Register / login / logout / user profile
Should succeed: create a new user with a new email; log in with the newly created user; log out the current authenticated user; update user profile legally (e.g. change password)
Should fail: create a new user with the same email; log in with incorrect password; update user profile illegally (e.g. change email to an existing email address)
Also show: user input validation (e.g., cannot register with an ill-formatted email); prevention of SQL injection (e.g., quotes and other special characters are handled safely)
Authenticated buyer
Should succeed: add products to carts / update carts; review products; checkout; view transaction history
Should fail: add unavailable product to cart; check out with insufficient balance (if any); accessing sensitive areas after signing out
Authenticated seller
Should succeed: manage inventory (e.g. add/delete products, change quantity); view order history
Should fail: add same product multiple times
Anything else you implemented or thought of during the demo

In addition, if you would like to be considered for the Audience and Staff Choice awards, please prepare an additional short video showcasing the highlights of your project (<5 minutes). This video can be more promotional in nature and does not need to show every detail of the project like your long demo video. We will post an Ed thread for sharing and voting on these short promotional videos.

Submit the following:
README.txt: as before, plus:
A link to your complete demo video.
REPORT.pdf: showing:
A refined database design, highlighting what has changed since the last submitted design.
The final list of features you have implemented or attempted to implement. For each feature, indicate its status: fully functional, buggy, partially implemented, or not implemented at all.
CODE.zip: all your code.
Grading Criteria
For the four milestones, points will be assigned mostly based on completion or effort made towards completion. Your design may not be perfect and your implementation may still have issues — that’s fine; we will give feedback but not take points off, unless there is clearly a lack of effort. The final product, however, will be graded according to its quality.
Milestone 1: 3 points
Milestone 2: 10 points (5 for database design and 5 for website design)
Milestone 3: 15 points (5 for video plus 2 per endpoint)
Milestone 4: 10 points (5 for video and 5 for the large testing database)
Final submission:
Report: 12 points (7 for video and 5 for the rest of the report)
Final product: 50 points

See Functionalities for features expected on your final product. Here we provide additional guidelines on how to break down the 50 points.
Team Score Option
A project with all 5 parts working together meeting the basic requirements will get you a baseline score of 43/50. Going above and beyond will earn points for your whole team, up to the maximum score of 50/50. Starting from the baseline:
(Basics) Buggy or missing features in the basic requirements for each team member’s part: -0.5 to -8 points, depending on how serious the issues are. You lose 8 points for each part that is totally missing.
(Integration) For each team member’s part that has buggy interaction with other parts or is not integrated into the final website: -0.5 to -1 point, depending on how serious the issues are. You can lose up to 5 points for lack of integration.
(Safety Penalty) Some code is susceptible to SQL injection attacks: -2 points overall.
(Style Penalty) Not following good coding practices (e.g., unnecessarily hard-coding values that should have been obtained from the database; excessive duplication of code without refactoring): -0.5 to -2 points overall, depending on how serious/prevalent the issue is.
(Performance Penalty) Unreasonably slow response time that could have been easily fixed (e.g., with appropriate database indexing, or by incrementally receiving and paginating results in the frontend): -0.5 to -1 point overall.
(Interaction Design Bonus) Well-designed, smooth user interaction: +0.5 to +1 point.
(Aesthetics Bonus) Well-designed and impressive-looking frontend: +0.5 to +2 points.
(Documentation Bonus) Commenting your code and documenting your design/setup (beyond what’s required in REPORT.pdf): +0.5 to +1 point.
(Data Bonus) Well-designed large testing database with real and/or realistic data: +0.5 to +2 points.
(Feature Bonus) Each additional feature: +0.5 to +2 points, depending on how impressive the added functionality is and how much effort it requires. Features that require extensive coordination among multiple teammates earn more.
You will not lose points by going with a plain-looking website coded in plain HTML. After all, this is not a course about web or frontend development!
Individual Score Option
Successfully meeting the basic requirements for your own part will give you a baseline score of 43/50. Going above and beyond the basic requirements, by yourself, can get you a maximum score of 47/50. In other words, getting a total project score in the high A/A+ range does require your whole team’s success! Starting from the baseline:
(Basics) Same as the guideline above for the team score option, but limit to your part and multiply the penalty by 5.
(Integration) Not applicable.
(Feature Bonus) In addition to the guideline above for the team score option, you can also earn bonuses for implementing basic features for other parts not assigned to you.
Other penalties and bonus: Same as the guideline above for the team score option.

</project_request>

<project_rules>

  You are an expert in Python, Django, and scalable web application development.

  Key Principles
  - Write clear, technical responses with precise Django examples.
  - Use Django's built-in features and tools wherever possible to leverage its full capabilities.
  - Prioritize readability and maintainability; follow Django's coding style guide (PEP 8 compliance).
  - Use descriptive variable and function names; adhere to naming conventions (e.g., lowercase with underscores for functions and variables).
  - Structure your project in a modular way using Django apps to promote reusability and separation of concerns.

  Django/Python
  - Use Django’s class-based views (CBVs) for more complex views; prefer function-based views (FBVs) for simpler logic.
  - Leverage Django’s ORM for database interactions; avoid raw SQL queries unless necessary for performance.
  - Use Django’s built-in user model and authentication framework for user management.
  - Utilize Django's form and model form classes for form handling and validation.
  - Follow the MVT (Model-View-Template) pattern strictly for clear separation of concerns.
  - Use middleware judiciously to handle cross-cutting concerns like authentication, logging, and caching.

  Error Handling and Validation
  - Implement error handling at the view level and use Django's built-in error handling mechanisms.
  - Use Django's validation framework to validate form and model data.
  - Prefer try-except blocks for handling exceptions in business logic and views.
  - Customize error pages (e.g., 404, 500) to improve user experience and provide helpful information.
  - Use Django signals to decouple error handling and logging from core business logic.

  Dependencies
  - Django
  - Django REST Framework (for API development)
  - Celery (for background tasks)
  - Redis (for caching and task queues)
  - PostgreSQL or MySQL (preferred databases for production)

  Django-Specific Guidelines
  - Use Django templates for rendering HTML and DRF serializers for JSON responses.
  - Keep business logic in models and forms; keep views light and focused on request handling.
  - Use Django's URL dispatcher (urls.py) to define clear and RESTful URL patterns.
  - Apply Django's security best practices (e.g., CSRF protection, SQL injection protection, XSS prevention).
  - Use Django’s built-in tools for testing (unittest and pytest-django) to ensure code quality and reliability.
  - Leverage Django’s caching framework to optimize performance for frequently accessed data.
  - Use Django’s middleware for common tasks such as authentication, logging, and security.

  Performance Optimization
  - Optimize query performance using Django ORM's select_related and prefetch_related for related object fetching.
  - Use Django’s cache framework with backend support (e.g., Redis or Memcached) to reduce database load.
  - Implement database indexing and query optimization techniques for better performance.
  - Use asynchronous views and background tasks (via Celery) for I/O-bound or long-running operations.
  - Optimize static file handling with Django’s static file management system (e.g., WhiteNoise or CDN integration).

  Key Conventions
  1. Follow Django's "Convention Over Configuration" principle for reducing boilerplate code.
  2. Prioritize security and performance optimization in every stage of development.
  3. Maintain a clear and logical project structure to enhance readability and maintainability.
  
  Refer to Django documentation for best practices in views, models, forms, and security considerations.
  
</project_rules>



<implementation_plan> not completed yet
In this task, I need to create a detailed technical specification for a Mini-Amazon project based on the instructions and project requirements provided in the instruction.md file. This specification should be comprehensive enough to serve as direct input for planning and code generation AI systems.

Let me break down the overall approach:

1. First, I'll analyze the project requirements and create a specification planning, considering architecture, features, database schema, etc.
2. Then, I'll develop a comprehensive technical specification following the markdown structure provided in the instructions.

The project is a Mini-Amazon e-commerce platform with these main components:
- Users/Account management (registration, login, balance management, purchase history)
- Products (browsing, searching, detailed views)
- Cart/Order (cart management, ordering, fulfillment)
- Sellers/Inventory (seller management, inventory, order fulfillment)
- Social/Feedback (ratings, reviews, messaging)

The technical stack includes Python, Django, and PostgreSQL.

Let me start with the specification planning:

## Core system architecture and key workflows
- Django MVT (Model-View-Template) architecture with Django REST Framework for API endpoints
- Key workflows include user registration/login, product browsing/searching, cart management, order placement/fulfillment, and review/rating submission
- Need to handle virtual currency transactions
- PostgreSQL for persistent data storage
- Session management for persistent cart state

## Project structure and organization
- Django project structure with separate apps for different components:
  - users (account management, authentication)
  - products (product listings, categories)
  - carts (cart management, orders)
  - sellers (inventory, fulfillment)
  - social (reviews, ratings, messaging)
- Static files organization for CSS, JavaScript, and images
- Templates organization for HTML templates
- URL routing structure across the entire application

## Detailed feature specifications
For each component, need to detail:
- Models and their relationships
- Views and templates
- Forms for data input
- API endpoints
- User workflows
- Error handling and edge cases

## Database schema design
- Users/Accounts tables
- Products and Categories tables
- Cart and Order tables
- Inventory tables
- Ratings and Reviews tables
- Messaging tables
- Relationships between these tables

## Server actions and integrations
- Authentication processes
- Search and filter functionality
- Cart management actions
- Order processing
- Virtual currency transactions
- Review and rating submission
- Inventory management

## Design system and component architecture
- Frontend layout and structure
- Responsive design considerations
- UI components and styling
- Django template organization
- JS interactions for dynamic elements

## Authentication and authorization implementation
- Django authentication system
- Login/registration flows
- User roles (regular user, seller)
- Permission handling for different actions

## Data flow and state management
- Server-side data handling with Django models
- Client-side state management where needed
- Cart state persistence
- Session management

## Payment implementation
- Virtual currency management
- Balance updates on transactions
- Transaction history tracking

## Analytics implementation
- Product and seller ratings aggregation
- Purchase history analysis
- User recommendations (optional feature)

## Testing strategy
- Unit tests for models and business logic
- Integration tests for views
- User interface testing

Now, I'll create the detailed technical specification following the provided structure.

# Mini-Amazon Technical Specification

## 1. System Overview
- Core purpose: Create a miniature version of Amazon where users can buy products from sellers using virtual currency
- Key workflows:
  - User registration and authentication
  - Product browsing, searching, and filtering
  - Cart management and order placement
  - Order fulfillment by sellers
  - Rating and review submission
  - Virtual currency management
- System architecture: Django MVT with PostgreSQL database

## 2. Project Structure
```
miniamazon/
├── manage.py
├── miniamazon/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── forms.py
│   └── views.py
├── products/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── forms.py
│   └── views.py
├── carts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── forms.py
│   └── views.py
├── sellers/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── forms.py
│   └── views.py
├── social/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── forms.py
│   └── views.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── users/
    ├── products/
    ├── carts/
    ├── sellers/
    └── social/
```

## 3. Feature Specification

### 3.1 Users and Accounts
- User story: As a user, I want to register an account, login, manage my profile, and track my balance and purchase history
- Requirements:
  - User registration with email, full name, address, and password
  - User login with email and password
  - Profile management (update name, address, password)
  - Balance management (view, add funds, withdraw)
  - Purchase history viewing and filtering
  - Public user profile view

#### Implementation Steps:
1. Create User model extending Django's AbstractUser
2. Implement registration and login views and forms
3. Create profile management views and forms
4. Implement balance management functionality
5. Create purchase history views with filtering options
6. Implement public profile view with conditional seller information

#### Error Handling and Edge Cases:
- Duplicate email registration attempt
- Invalid login credentials
- Insufficient balance for withdrawals or purchases
- Session expiration handling

### 3.2 Products
- User story: As a user, I want to browse products by category, search for specific products, view detailed product information, and create new product listings
- Requirements:
  - Product categories with browsing capability
  - Product search and filtering by keywords, price, etc.
  - Detailed product pages showing all information and sellers
  - Product creation and editing functionality

#### Implementation Steps:
1. Create Category and Product models
2. Implement category browsing views
3. Create search functionality with filters
4. Design detailed product page with seller information
5. Implement product creation and editing forms and views

#### Error Handling and Edge Cases:
- No products found in search
- Invalid product data submission
- Unauthorized product editing attempts
- Image upload failures

### 3.3 Cart and Orders
- User story: As a buyer, I want to add products to my cart, manage cart contents, place orders, and track order status
- Requirements:
  - Add products to cart from product pages
  - View and edit cart contents
  - Submit orders with inventory and balance verification
  - View order history and details
  - Order status tracking

#### Implementation Steps:
1. Create Cart, CartItem, Order, and OrderItem models
2. Implement cart management views and forms
3. Create order submission process with validation
4. Design order history and detail views
5. Implement order status tracking

#### Error Handling and Edge Cases:
- Insufficient inventory for order
- Insufficient balance for order
- Changed prices or inventory during order process
- Cart session persistence issues

### 3.4 Inventory and Order Fulfillment
- User story: As a seller, I want to manage my inventory and fulfill orders
- Requirements:
  - Inventory management interface
  - Order fulfillment workflow
  - Order history for sellers

#### Implementation Steps:
1. Create Inventory model linked to User and Product
2. Implement inventory management views and forms
3. Create seller's order view with fulfillment actions
4. Design order fulfillment workflow

#### Error Handling and Edge Cases:
- Trying to add duplicate products to inventory
- Negative inventory quantities
- Conflicts in order fulfillment

### 3.5 Feedback and Messaging
- User story: As a user, I want to rate and review products and sellers, and potentially message sellers about orders
- Requirements:
  - Product rating and review system
  - Seller rating and review system
  - Optional: Messaging system between buyers and sellers

#### Implementation Steps:
1. Create ProductReview and SellerReview models
2. Implement review submission forms and views
3. Create review display components for products and sellers
4. Optional: Implement messaging system with Message and Thread models

#### Error Handling and Edge Cases:
- Multiple review attempts for same product/seller
- Invalid rating submissions
- Inappropriate content handling

## 4. Database Schema

### 4.1 Tables

#### User
- id (PK, AutoField): Unique identifier for the user
- email (EmailField, unique): User's email address
- password (CharField): User's hashed password
- full_name (CharField): User's full name
- address (TextField): User's shipping address
- balance (DecimalField): User's current balance of virtual currency
- created_at (DateTimeField): When the user was created
- updated_at (DateTimeField): When the user was last updated

#### Category
- id (PK, AutoField): Unique identifier for the category
- name (CharField): Name of the category
- description (TextField): Description of the category

#### Product
- id (PK, AutoField): Unique identifier for the product
- name (CharField): Name of the product
- description (TextField): Description of the product
- category (FK to Category): Product category
- image (ImageField): Product image
- created_by (FK to User): User who created the product
- created_at (DateTimeField): When the product was created
- updated_at (DateTimeField): When the product was last updated

#### Inventory
- id (PK, AutoField): Unique identifier for the inventory item
- seller (FK to User): User selling the product
- product (FK to Product): Product being sold
- quantity (PositiveIntegerField): Available quantity
- price (DecimalField): Price per unit
- created_at (DateTimeField): When the inventory was created
- updated_at (DateTimeField): When the inventory was last updated

#### Cart
- id (PK, AutoField): Unique identifier for the cart
- user (FK to User): User who owns the cart
- created_at (DateTimeField): When the cart was created
- updated_at (DateTimeField): When the cart was last updated

#### CartItem
- id (PK, AutoField): Unique identifier for the cart item
- cart (FK to Cart): Cart containing this item
- inventory (FK to Inventory): Inventory item being referenced
- quantity (PositiveIntegerField): Quantity in cart
- created_at (DateTimeField): When the cart item was created
- updated_at (DateTimeField): When the cart item was last updated

#### Order
- id (PK, AutoField): Unique identifier for the order
- user (FK to User): User who placed the order
- total_amount (DecimalField): Total order amount
- is_fulfilled (BooleanField): Whether the entire order is fulfilled
- created_at (DateTimeField): When the order was created
- updated_at (DateTimeField): When the order was last updated

#### OrderItem
- id (PK, AutoField): Unique identifier for the order item
- order (FK to Order): Order containing this item
- inventory (FK to Inventory): Inventory item being referenced
- quantity (PositiveIntegerField): Quantity ordered
- unit_price (DecimalField): Price per unit at time of order
- is_fulfilled (BooleanField): Whether this item is fulfilled
- fulfilled_at (DateTimeField, nullable): When the item was fulfilled
- created_at (DateTimeField): When the order item was created

#### ProductReview
- id (PK, AutoField): Unique identifier for the product review
- product (FK to Product): Product being reviewed
- user (FK to User): User writing the review
- rating (PositiveSmallIntegerField): Rating (1-5)
- comment (TextField): Review comment
- created_at (DateTimeField): When the review was created
- updated_at (DateTimeField): When the review was last updated

#### SellerReview
- id (PK, AutoField): Unique identifier for the seller review
- seller (FK to User): Seller being reviewed
- user (FK to User): User writing the review
- order (FK to Order): Order related to this review
- rating (PositiveSmallIntegerField): Rating (1-5)
- comment (TextField): Review comment
- created_at (DateTimeField): When the review was created
- updated_at (DateTimeField): When the review was last updated

#### Message (Optional)
- id (PK, AutoField): Unique identifier for the message
- sender (FK to User): User sending the message
- receiver (FK to User): User receiving the message
- order (FK to Order): Related order
- content (TextField): Message content
- is_read (BooleanField): Whether the message has been read
- created_at (DateTimeField): When the message was created

## 5. Server Actions

### 5.1 Database Actions

#### User Registration
- Description: Create a new user account
- Input: email, full_name, address, password
- Return: User object, success/error message
- ORM Operation:
```python
User.objects.create_user(
    email=email,
    full_name=full_name,
    address=address,
    password=password,
    balance=0
)
```

#### User Login
- Description: Authenticate a user
- Input: email, password
- Return: User object, success/error message
- Django Authentication:
```python
from django.contrib.auth import authenticate, login
user = authenticate(request, email=email, password=password)
if user is not None:
    login(request, user)
    # Redirect to success page
else:
    # Return error message
```

#### Update User Profile
- Description: Update user information
- Input: user_id, full_name, address, password (optional)
- Return: Updated User object, success/error message
- ORM Operation:
```python
user = User.objects.get(id=user_id)
user.full_name = full_name
user.address = address
if password:
    user.set_password(password)
user.save()
```

#### Update User Balance
- Description: Add or withdraw funds from user balance
- Input: user_id, amount, is_addition
- Return: Updated User object, success/error message
- ORM Operation:
```python
user = User.objects.get(id=user_id)
if is_addition:
    user.balance += amount
else:
    if user.balance >= amount:
        user.balance -= amount
    else:
        # Return error message
user.save()
```

#### Get User Purchase History
- Description: Retrieve purchase history for a user
- Input: user_id, optional filters
- Return: List of Order objects
- ORM Operation:
```python
orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
# Apply additional filters if provided
```

#### Create Product
- Description: Create a new product
- Input: name, description, category_id, image, created_by_id
- Return: Product object, success/error message
- ORM Operation:
```python
product = Product.objects.create(
    name=name,
    description=description,
    category_id=category_id,
    image=image,
    created_by_id=created_by_id
)
```

#### Update Product
- Description: Update product information
- Input: product_id, name, description, category_id, image
- Return: Updated Product object, success/error message
- ORM Operation:
```python
product = Product.objects.get(id=product_id)
product.name = name
product.description = description
product.category_id = category_id
if image:
    product.image = image
product.save()
```

#### Search Products
- Description: Search for products by keywords, category, or other filters
- Input: query, category_id, min_price, max_price, sort_by
- Return: List of Product objects
- ORM Operation:
```python
products = Product.objects.all()
if query:
    products = products.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
if category_id:
    products = products.filter(category_id=category_id)
if min_price:
    products = products.filter(inventory__price__gte=min_price)
if max_price:
    products = products.filter(inventory__price__lte=max_price)
if sort_by == 'price_asc':
    products = products.order_by('inventory__price')
elif sort_by == 'price_desc':
    products = products.order_by('-inventory__price')
# Remove duplicates due to multiple inventory items
products = products.distinct()
```

#### Add to Cart
- Description: Add a product to user's cart
- Input: user_id, inventory_id, quantity
- Return: Updated Cart object, success/error message
- ORM Operation:
```python
cart, created = Cart.objects.get_or_create(user_id=user_id)
inventory = Inventory.objects.get(id=inventory_id)
if inventory.quantity >= quantity:
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        inventory=inventory,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
else:
    # Return error message
```

#### Update Cart Item
- Description: Update quantity of an item in cart
- Input: cart_item_id, quantity
- Return: Updated CartItem object, success/error message
- ORM Operation:
```python
cart_item = CartItem.objects.get(id=cart_item_id)
if quantity <= 0:
    cart_item.delete()
else:
    inventory = cart_item.inventory
    if inventory.quantity >= quantity:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        # Return error message
```

#### Place Order
- Description: Convert cart to order
- Input: user_id
- Return: Order object, success/error message
- ORM Operation: Transaction with multiple steps:
```python
from django.db import transaction

with transaction.atomic():
    user = User.objects.select_for_update().get(id=user_id)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('inventory')
    
    # Calculate total and check inventory and balance
    total_amount = sum(item.inventory.price * item.quantity for item in cart_items)
    if user.balance < total_amount:
        # Return error message
        
    # Check inventory quantities
    for item in cart_items:
        if item.inventory.quantity < item.quantity:
            # Return error message
    
    # Create order
    order = Order.objects.create(
        user=user,
        total_amount=total_amount
    )
    
    # Create order items and update inventory
    for cart_item in cart_items:
        inventory = cart_item.inventory
        OrderItem.objects.create(
            order=order,
            inventory=inventory,
            quantity=cart_item.quantity,
            unit_price=inventory.price
        )
        inventory.quantity -= cart_item.quantity
        inventory.save()
        
        # Update seller balance
        seller = inventory.seller
        seller.balance += inventory.price * cart_item.quantity
        seller.save()
    
    # Update buyer balance
    user.balance -= total_amount
    user.save()
    
    # Clear cart
    cart_items.delete()
```

#### Fulfill Order Item
- Description: Mark an order item as fulfilled
- Input: order_item_id
- Return: Updated OrderItem object, success/error message
- ORM Operation:
```python
from django.utils import timezone

order_item = OrderItem.objects.get(id=order_item_id)
order_item.is_fulfilled = True
order_item.fulfilled_at = timezone.now()
order_item.save()

# Check if all items in the order are fulfilled
order = order_item.order
all_items_fulfilled = not OrderItem.objects.filter(
    order=order, is_fulfilled=False
).exists()
if all_items_fulfilled:
    order.is_fulfilled = True
    order.save()
```

#### Add Product to Inventory
- Description: Add a product to seller's inventory
- Input: seller_id, product_id, quantity, price
- Return: Inventory object, success/error message
- ORM Operation:
```python
inventory, created = Inventory.objects.get_or_create(
    seller_id=seller_id,
    product_id=product_id,
    defaults={
        'quantity': quantity,
        'price': price
    }
)
if not created:
    inventory.quantity += quantity
    inventory.price = price  # Update price to the new price
    inventory.save()
```

#### Update Inventory
- Description: Update inventory quantity and price
- Input: inventory_id, quantity, price
- Return: Updated Inventory object, success/error message
- ORM Operation:
```python
inventory = Inventory.objects.get(id=inventory_id)
inventory.quantity = quantity
inventory.price = price
inventory.save()
```

#### Create Product Review
- Description: Submit a review for a product
- Input: product_id, user_id, rating, comment
- Return: ProductReview object, success/error message
- ORM Operation:
```python
review, created = ProductReview.objects.get_or_create(
    product_id=product_id,
    user_id=user_id,
    defaults={
        'rating': rating,
        'comment': comment
    }
)
if not created:
    review.rating = rating
    review.comment = comment
    review.save()
```

#### Create Seller Review
- Description: Submit a review for a seller
- Input: seller_id, user_id, order_id, rating, comment
- Return: SellerReview object, success/error message
- ORM Operation:
```python
review, created = SellerReview.objects.get_or_create(
    seller_id=seller_id,
    user_id=user_id,
    order_id=order_id,
    defaults={
        'rating': rating,
        'comment': comment
    }
)
if not created:
    review.rating = rating
    review.comment = comment
    review.save()
```

### 5.2 Other Actions

#### Image Upload Handling
- Description: Handle product image uploads
- Process:
  1. Validate image type and size
  2. Generate a unique filename
  3. Save the image to the media directory
  4. Return the image path for storage in the database

#### Email Notifications (Optional)
- Description: Send email notifications for various events
- Events:
  - User registration
  - Order placement
  - Order fulfillment
  - Balance updates

#### Product Recommendation Algorithm (Optional)
- Description: Generate product recommendations for users
- Process:
  1. Analyze user purchase history
  2. Find similar products based on category and purchase patterns
  3. Return a list of recommended products

## 6. Design System

### 6.1 Visual Style
- Color Palette:
  - Primary: #232F3E (Amazon blue)
  - Secondary: #FF9900 (Amazon orange)
  - Accent: #37475A (Dark blue)
  - Background: #FFFFFF (White)
  - Text: #333333 (Dark gray)
  - Success: #007600 (Green)
  - Warning: #FF5500 (Orange)
  - Error: #B12704 (Red)
- Typography:
  - Primary Font: 'Arial', sans-serif
  - Headings: 18-24px, bold
  - Body Text: 14-16px, regular
  - Small Text: 12px, light
- Spacing:
  - Base Unit: 8px
  - Padding: 16px for containers, 8px for elements
  - Margins: 16px between sections, 8px between elements

### 6.2 Core Components
- Navigation:
  - Top navbar with logo, search, cart, and user account links
  - Category navigation sidebar
- Cards:
  - Product cards with image, title, price, and rating
  - Review cards with rating, comment, and user information
- Forms:
  - Input fields with labels and validation messages
  - Buttons: primary, secondary, and tertiary styles
- Tables:
  - Order history tables
  - Inventory management tables

## 7. Component Architecture

### 7.1 Server Components
- User Authentication Views:
  - LoginView: Handle user login
  - RegisterView: Handle user registration
  - ProfileView: Display and update user profile
- Product Views:
  - ProductListView: Display products with filters
  - ProductDetailView: Display detailed product information
  - ProductCreateView: Handle product creation
- Cart Views:
  - CartView: Display cart contents
  - AddToCartView: Handle adding items to cart
  - UpdateCartView: Handle updating cart items
- Order Views:
  - OrderListView: Display order history
  - OrderDetailView: Display detailed order information
  - OrderCreateView: Handle order creation
- Inventory Views:
  - InventoryListView: Display seller's inventory
  - InventoryCreateView: Handle adding products to inventory
  - InventoryUpdateView: Handle updating inventory
- Review Views:
  - ProductReviewCreateView: Handle product review submission
  - SellerReviewCreateView: Handle seller review submission

### 7.2 Client Components
- Product Search Component:
  - Keyword input
  - Category filter
  - Price range filter
  - Sort options
- Product Detail Component:
  - Product information display
  - Seller selection
  - Quantity selection
  - Add to cart button
- Cart Component:
  - Cart item listing
  - Quantity adjustment
  - Removal capability
  - Checkout button
- Order Summary Component:
  - Order items listing
  - Total calculation
  - Order status display
- Review Form Component:
  - Rating selection
  - Comment input
  - Submission button

## 8. Authentication & Authorization
- Django Authentication System:
  - User model extending AbstractUser
  - Authentication middleware
  - Login and registration views
- Permission Management:
  - View-level permissions for protected pages
  - Model-level permissions for data access
  - Custom permission for seller actions
- Session Management:
  - Django's built-in session framework
  - Shopping cart persistence

## 9. Data Flow
- Server-side Data Flow:
  - HTTP request → URL routing → View processing → Template rendering → HTTP response
  - Form submission → Validation → Database update → Redirect
- Client-side Data Flow:
  - User interaction → Form submission → Server processing → Page update
  - AJAX requests for dynamic updates (optional)

## 10. Virtual Currency Integration
- Balance Management:
  - Add funds function
  - Withdraw funds function
  - Transaction recording
- Transaction Processing:
  - Order placement: Buyer balance check and update
  - Order fulfillment: Seller balance update

## 11. Analytics Implementation (Optional)
- Product Analytics:
  - Most viewed products
  - Most purchased products
  - Highest rated products
- User Analytics:
  - Purchase patterns
  - Category preferences
  - Spending habits
- Seller Analytics:
  - Sales performance
  - Inventory turnover
  - Rating trends

## 12. Testing
- Unit Tests:
  - Model tests for data validation and relationships
  - Form tests for validation logic
  - View tests for HTTP responses and context data
- Integration Tests:
  - User registration and login flow
  - Product search and filtering
  - Cart management and checkout
  - Order placement and fulfillment
- UI Tests:
  - Form submission and validation
  - Navigation and routing
  - Error message display

This comprehensive technical specification provides a detailed blueprint for implementing the Mini-Amazon project with Django and PostgreSQL. It covers all the required functionalities and provides clear implementation guidance for each component.
</think>

I'll create a detailed technical specification for the Mini-Amazon project based on the requirements provided.

<specification_planning>
# Planning for Mini-Amazon Technical Specification

## 1. Core System Architecture and Key Workflows
- Django MVT architecture with PostgreSQL database
- Main components: Users, Products, Carts, Sellers, Social
- Key workflows:
  - User registration/authentication
  - Product browsing/searching/filtering
  - Cart management and checkout
  - Order processing and fulfillment
  - Review/rating submission
  - Balance management

## 2. Project Structure and Organization
- Django project with 5 main apps:
  - users: Account management, authentication, balance
  - products: Product listings, categories, search
  - carts: Cart management, order processing
  - sellers: Inventory management, order fulfillment
  - social: Ratings, reviews, messaging
- Structured following Django conventions with models, views, templates, forms
- Static files organization and template hierarchy

## 3. Detailed Feature Specifications
### Users
- Registration with email validation
- Profile management with address and payment info
- Balance management system (add/withdraw)
- Purchase history tracking

### Products
- Category-based organization
- Search and filter functionality
- Product detail pages
- Product creation/editing (for sellers)

### Carts
- Session-based cart persistence
- Cart item management
- Checkout process with validation
- Order history and status tracking

### Sellers
- Inventory management interface
- Order fulfillment workflow
- Sales analytics

### Social
- Product and seller review systems
- Messaging system (optional)
- Rating aggregation and display

## 4. Database Schema Design
- User model (extending Django's AbstractUser)
- Product and Category models
- Cart and CartItem models
- Order and OrderItem models
- Inventory model
- Review models (ProductReview, SellerReview)
- Message model (optional)
- Clear relationships between models with appropriate foreign keys

## 5. Server Actions and Integrations
- Authentication flows
- Product CRUD operations
- Cart management actions
- Order processing with transaction management
- Review submission and validation
- Virtual currency transactions

## 6. Design System and Component Architecture
- Responsive layout with Bootstrap or custom CSS
- Consistent UI components
- Form design and validation feedback
- Navigation structure

## 7. Authentication and Authorization Implementation
- Django's authentication framework
- Custom permissions for seller vs. buyer actions
- Protected views based on authentication status

## 8. Data Flow and State Management
- Server-side state management with Django
- Session management for cart persistence
- Form handling and validation

## 9. Payment Implementation
- Virtual currency system with transactions
- Balance updates on purchases and sales
- Transaction history

## 10. Analytics Implementation
- Basic analytics for product popularity
- Seller performance metrics
- Optional recommendation system

## 11. Testing Strategy
- Unit tests for models and business logic
- Integration tests for views and forms
- UI testing with Django test client
- Test data generation

## Challenges and Considerations
- Ensuring transaction integrity during purchases
- Handling race conditions with inventory
- Efficient query optimization for product listings
- Proper error handling across all workflows
- User experience for the shopping process
</specification_planning>

```markdown
# Mini-Amazon Technical Specification

## 1. System Overview

### Core Purpose and Value Proposition
Mini-Amazon is a web application that simulates key features of Amazon, allowing users to create accounts, browse and purchase products from various sellers using virtual currency, write reviews, and interact with sellers. The platform provides a complete e-commerce experience with product listings, shopping carts, order processing, inventory management, and a social feedback system.

### Key Workflows

1. **User Registration and Authentication**
   - User registers with email, name, address, and password
   - User logs in with credentials
   - User manages profile and balance

2. **Product Management**
   - Users browse products by category
   - Users search for products with filters
   - Sellers create and manage product listings
   - Users view detailed product information

3. **Shopping Experience**
   - Users add products to cart
   - Users manage cart contents
   - Users check out and place orders
   - System verifies balance and inventory

4. **Order Fulfillment**
   - Sellers view orders to fulfill
   - Sellers mark items as fulfilled
   - Buyers track order status
   - System updates order status

5. **Feedback System**
   - Users rate and review products
   - Users rate and review sellers
   - System aggregates ratings
   - Optional: Users message sellers about orders

### System Architecture

The application follows the Django Model-View-Template (MVT) architecture:

- **Models**: Define database schema for users, products, orders, etc.
- **Views**: Handle HTTP requests and business logic
- **Templates**: Render HTML responses to users

The system uses:
- **Django**: Web framework for backend
- **PostgreSQL**: Relational database
- **Django Forms**: For input validation and processing
- **Django Authentication**: For user management
- **Django ORM**: For database interactions
- **Bootstrap/CSS**: For frontend styling

## 2. Project Structure

```
miniamazon/
├── manage.py                     # Django management script
├── miniamazon/                   # Project configuration
│   ├── __init__.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
├── users/                        # User management app
│   ├── __init__.py
│   ├── admin.py                  # Admin configuration
│   ├── apps.py                   # App configuration
│   ├── forms.py                  # User-related forms
│   ├── migrations/               # Database migrations
│   ├── models.py                 # User data models
│   ├── templates/users/          # User-related templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── purchase_history.html
│   ├── tests.py                  # Tests for users app
│   ├── urls.py                   # User-related URLs
│   └── views.py                  # User-related views
├── products/                     # Products app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                  # Product-related forms
│   ├── migrations/
│   ├── models.py                 # Product data models
│   ├── templates/products/       # Product-related templates
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   └── product_create.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── carts/                        # Cart and order app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py                 # Cart and order models
│   ├── templates/carts/          # Cart-related templates
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_list.html
│   │   └── order_detail.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── sellers/                      # Sellers app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py                 # Inventory models
│   ├── templates/sellers/        # Seller-related templates
│   │   ├── inventory.html
│   │   ├── fulfillment.html
│   │   └── sales_history.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── social/                       # Social features app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py                 # Review and message models
│   ├── templates/social/         # Social-related templates
│   │   ├── product_review.html
│   │   ├── seller_review.html
│   │   └── messages.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/                       # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo.png
├── templates/                    # Project-wide templates
│   ├── base.html                 # Base template
│   ├── home.html                 # Homepage
│   └── includes/                 # Reusable template parts
│       ├── navbar.html
│       └── footer.html
├── media/                        # User-uploaded files
│   └── products/                 # Product images
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## 3. Feature Specification

### 3.1 Account/User Management

#### User Story and Requirements
As a user, I want to register, login, manage my profile, track my balance, and view my purchase history.

- User registration with email, password, name, and address
- User login and authentication
- Profile management
- Balance management (add/withdraw virtual currency)
- Purchase history tracking

#### Detailed Implementation Steps

1. **User Registration**
   - Create registration form with email, password, full name, address
   - Validate email uniqueness
   - Implement password hashing
   - Create user account with initial $0 balance
   - Redirect to profile page after successful registration

2. **User Login**
   - Create login form with email and password
   - Authenticate using Django's authentication system
   - Create session for logged-in user
   - Redirect to previous page or home page

3. **Profile Management**
   - Create profile form with editable fields (name, address, password)
   - Implement profile update view
   - Add validation for all fields
   - Show success message upon update

4. **Balance Management**
   - Create forms for adding and withdrawing funds
   - Implement balance update view
   - Validate withdrawal amount against current balance
   - Record transaction history

5. **Purchase History**
   - Create view for listing all user orders
   - Implement sorting (default: reverse chronological)
   - Add filtering options by date, seller, status
   - Link to detailed order view

#### Error Handling and Edge Cases
- Duplicate email registration attempts: Return validation error
- Invalid login credentials: Show appropriate error message
- Password mismatch during registration/update: Validate and show error
- Insufficient balance for withdrawal: Show error and prevent transaction
- Expired sessions: Redirect to login with return URL

### 3.2 Products

#### User Story and Requirements
As a user, I want to browse products by category, search with filters, view detailed product information, and create/edit my own product listings.

- Predefined product categories
- Product browsing with search and filters
- Detailed product pages showing product info and sellers
- Product creation and editing

#### Detailed Implementation Steps

1. **Category Management**
   - Create predefined product categories
   - Implement category browsing view
   - Show product counts per category

2. **Product Listing**
   - Create product list view with pagination
   - Implement search by keywords
   - Add filters for category, price range
   - Add sorting options (price, rating)
   - Display product summaries with images

3. **Product Detail**
   - Create detailed product view
   - Show all product information (name, description, image)
   - List all sellers with prices and inventory levels
   - Display average rating and reviews
   - Add interface for adding to cart

4. **Product Creation/Editing**
   - Create product form with all required fields
   - Implement image upload handling
   - Add validation for all fields
   - Restrict editing to product creator

#### Error Handling and Edge Cases
- Invalid product data: Validate and show errors
- Missing required fields: Prevent submission
- Image upload failures: Handle and show appropriate error
- Unauthorized edit attempts: Check permissions and redirect
- Product not found: Show 404 page

### 3.3 Cart and Orders

#### User Story and Requirements
As a user, I want to add products to my cart, manage cart contents, place orders, and track order status.

- Session-persistent shopping cart
- Cart item management (add, update, remove)
- Checkout process with balance and inventory validation
- Order history and status tracking

#### Detailed Implementation Steps

1. **Cart Management**
   - Create cart model associated with user
   - Implement add-to-cart functionality from product pages
   - Create cart detail view showing all items
   - Add quantity adjustment and removal options
   - Calculate and display total price

2. **Checkout Process**
   - Create checkout view with order summary
   - Validate inventory availability for all items
   - Validate user balance against total amount
   - Implement transaction management for order creation
   - Update balances and inventory upon successful order

3. **Order Processing**
   - Create OrderItem model to track individual items
   - Update seller balance for each item
   - Reduce inventory quantities
   - Empty cart after successful order
   - Redirect to order confirmation page

4. **Order History**
   - Create order list view for user
   - Implement order detail view showing all items
   - Display fulfillment status for each item
   - Update order status based on item fulfillment

#### Error Handling and Edge Cases
- Insufficient inventory: Check and show error during checkout
- Insufficient balance: Validate and prevent order submission
- Price changes during checkout: Revalidate prices before finalizing
- Empty cart checkout attempt: Prevent and redirect
- Session expiration: Persist cart data to database for logged-in users

### 3.4 Inventory and Order Fulfillment

#### User Story and Requirements
As a seller, I want to manage my inventory and fulfill orders placed by buyers.

- Inventory management interface
- Product listing in inventory
- Order fulfillment workflow
- Sales history tracking

#### Detailed Implementation Steps

1. **Inventory Management**
   - Create inventory model linked to seller and product
   - Implement inventory list view for seller
   - Add inventory creation/update forms
   - Validate inventory quantities (prevent negative)
   - Add removal functionality

2. **Order Fulfillment**
   - Create fulfillment view showing pending orders
   - Filter orders by status
   - Implement fulfillment action for individual items
   - Update order status when all items fulfilled
   - Send notification to buyer (optional)

3. **Sales Analytics**
   - Create sales history view
   - Implement filtering and sorting options
   - Show key metrics (total sales, average rating)
   - Display visualizations (optional)

#### Error Handling and Edge Cases
- Duplicate product in inventory: Update quantity instead of creating new
- Negative inventory values: Validate and prevent
- Fulfilling already fulfilled items: Check status before action
- Conflicting fulfillment attempts: Implement locking mechanism

### 3.5 Feedback and Messaging

#### User Story and Requirements
As a user, I want to rate and review products and sellers, and potentially communicate with sellers about orders.

- Product rating and review system
- Seller rating and review system
- Rating aggregation and display
- Optional: Messaging system between buyers and sellers

#### Detailed Implementation Steps

1. **Product Reviews**
   - Create product review model with rating and comment
   - Implement review submission form
   - Validate one review per user per product
   - Add editing and deletion capabilities
   - Display average rating on product pages

2. **Seller Reviews**
   - Create seller review model linked to orders
   - Implement review submission form
   - Validate that user has purchased from seller
   - Display average rating on seller profiles
   - Add editing and deletion capabilities

3. **Review Management**
   - Create user's reviews list view
   - Implement filtering and sorting options
   - Add editing interface
   - Validate review ownership

4. **Messaging System (Optional)**
   - Create message model between users
   - Implement thread-based messaging
   - Add notifications for new messages
   - Ensure privacy between buyer and seller

#### Error Handling and Edge Cases
- Multiple review attempts: Check existing reviews
- Reviews without purchases: Validate order history
- Inappropriate content: Implement moderation (optional)
- Missing rating or required fields: Validate submission

## 4. Database Schema

### 4.1 Tables

#### User
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `email` (EmailField, unique): User's email address
  - `password` (CharField): Hashed password
  - `full_name` (CharField): User's full name
  - `address` (TextField): Shipping address
  - `balance` (DecimalField): Current virtual currency balance
  - `date_joined` (DateTimeField): Account creation timestamp
  - `last_login` (DateTimeField): Last login timestamp
  - `is_active` (BooleanField): Account status

- **Relationships**
  - One-to-many with Cart (user has one cart)
  - One-to-many with Order (user has many orders)
  - One-to-many with Inventory (user has many inventory items as seller)
  - One-to-many with ProductReview (user has many product reviews)
  - One-to-many with SellerReview (user has many seller reviews)

- **Indexes**
  - Index on `email` for login queries
  - Index on `id` for relationship lookups

#### Category
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `name` (CharField): Category name
  - `description` (TextField): Category description
  - `created_at` (DateTimeField): Creation timestamp

- **Relationships**
  - One-to-many with Product (category has many products)

- **Indexes**
  - Index on `name` for search queries

#### Product
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `name` (CharField): Product name
  - `description` (TextField): Product description
  - `image` (ImageField): Product image
  - `category_id` (FK to Category): Category of product
  - `created_by_id` (FK to User): User who created the product
  - `created_at` (DateTimeField): Creation timestamp
  - `updated_at` (DateTimeField): Last update timestamp

- **Relationships**
  - Many-to-one with Category (product belongs to one category)
  - Many-to-one with User (product created by one user)
  - One-to-many with Inventory (product has many inventory listings)
  - One-to-many with ProductReview (product has many reviews)

- **Indexes**
  - Index on `name` for search queries
  - Index on `category_id` for category filtering
  - Index on `created_by_id` for user's products

#### Inventory
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `seller_id` (FK to User): User selling the product
  - `product_id` (FK to Product): Product being sold
  - `quantity` (PositiveIntegerField): Available quantity
  - `price` (DecimalField): Price per unit
  - `created_at` (DateTimeField): Creation timestamp
  - `updated_at` (DateTimeField): Last update timestamp

- **Relationships**
  - Many-to-one with User (inventory belongs to one seller)
  - Many-to-one with Product (inventory is for one product)
  - One-to-many with CartItem (inventory has many cart items)
  - One-to-many with OrderItem (inventory has many order items)

- **Indexes**
  - Composite index on `seller_id` and `product_id` for uniqueness
  - Index on `product_id` for product inventory queries
  - Index on `seller_id` for seller inventory queries

#### Cart
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `user_id` (FK to User): User who owns the cart
  - `created_at` (DateTimeField): Creation timestamp
  - `updated_at` (DateTimeField): Last update timestamp

- **Relationships**
  - Many-to-one with User (cart belongs to one user)
  - One-to-many with CartItem (cart has many items)

- **Indexes**
  - Index on `user_id` for user's cart lookup

#### CartItem
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `cart_id` (FK to Cart): Cart containing this item
  - `inventory_id` (FK to Inventory): Inventory item being referenced
  - `quantity` (PositiveIntegerField): Quantity in cart
  - `created_at` (DateTimeField): Creation timestamp
  - `updated_at` (DateTimeField): Last update timestamp

- **Relationships**
  - Many-to-one with Cart (item belongs to one cart)
  - Many-to-one with Inventory (item references one inventory listing)

- **Indexes**
  - Composite index on `cart_id` and `inventory_id` for uniqueness
  - Index on `cart_id` for cart items lookup

#### Order
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `user_id` (FK to User): User who placed the order
  - `total_amount` (DecimalField): Total order amount
  - `is_fulfilled` (BooleanField): Whether the entire order is fulfilled
  - `created_at` (DateTimeField): When the order was created
  - `updated_at` (DateTimeField): When the order was last updated

- **Relationships**
  - Many-to-one with User (order belongs to one user)
  - One-to-many with OrderItem (order has many items)
  - One-to-many with SellerReview (order has many seller reviews)

- **Indexes**
  - Index on `user_id` for user's orders lookup
  - Index on `created_at` for order history sorting

#### OrderItem
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `order_id` (FK to Order): Order containing this item
  - `inventory_id` (FK to Inventory): Inventory item being referenced
  - `quantity` (PositiveIntegerField): Quantity ordered
  - `unit_price` (DecimalField): Price per unit at time of order
  - `is_fulfilled` (BooleanField): Whether this item is fulfilled
  - `fulfilled_at` (DateTimeField, nullable): When the item was fulfilled
  - `created_at` (DateTimeField): When the order item was created

- **Relationships**
  - Many-to-one with Order (item belongs to one order)
  - Many-to-one with Inventory (item references one inventory listing)

- **Indexes**
  - Index on `order_id` for order items lookup
  - Index on `inventory_id` for seller's order items lookup
  - Index on `is_fulfilled` for fulfillment status filtering

#### ProductReview
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `product_id` (FK to Product): Product being reviewed
  - `user_id` (FK to User): User writing the review
  - `rating` (PositiveSmallIntegerField): Rating (1-5)
  - `comment` (TextField): Review comment
  - `created_at` (DateTimeField): When the review was created
  - `updated_at` (DateTimeField): When the review was last updated

- **Relationships**
  - Many-to-one with Product (review is for one product)
  - Many-to-one with User (review is by one user)

- **Indexes**
  - Composite index on `product_id` and `user_id` for uniqueness
  - Index on `product_id` for product reviews lookup
  - Index on `user_id` for user's reviews lookup
  - Index on `rating` for rating filtering

#### SellerReview
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `seller_id` (FK to User): Seller being reviewed
  - `user_id` (FK to User): User writing the review
  - `order_id` (FK to Order): Order related to this review
  - `rating` (PositiveSmallIntegerField): Rating (1-5)
  - `comment` (TextField): Review comment
  - `created_at` (DateTimeField): When the review was created
  - `updated_at` (DateTimeField): When the review was last updated

- **Relationships**
  - Many-to-one with User (seller) (review is for one seller)
  - Many-to-one with User (buyer) (review is by one user)
  - Many-to-one with Order (review is related to one order)

- **Indexes**
  - Composite index on `seller_id` and `order_id` for uniqueness
  - Index on `seller_id` for seller reviews lookup
  - Index on `user_id` for user's reviews lookup
  - Index on `rating` for rating filtering

#### Message (Optional)
- **Fields**
  - `id` (PK, AutoField): Unique identifier
  - `sender_id` (FK to User): User sending the message
  - `receiver_id` (FK to User): User receiving the message
  - `order_id` (FK to Order): Related order
  - `content` (TextField): Message content
  - `is_read` (BooleanField): Whether the message has been read
  - `created_at` (DateTimeField): When the message was created

- **Relationships**
  - Many-to-one with User (sender) (message from one user)
  - Many-to-one with User (receiver) (message to one user)
  - Many-to-one with Order (message related to one order)

- **Indexes**
  - Index on `sender_id` for sent messages lookup
  - Index on `receiver_id` for received messages lookup
  - Index on `order_id` for order messages lookup
  - Index on `is_read` for unread messages filtering

## 5. Server Actions

### 5.1 Database Actions

#### User Registration
- **Description**: Create a new user account
- **Input Parameters**: 
  - `email`: User's email address
  - `password`: User's password
  - `full_name`: User's full name
  - `address`: User's address
- **Return Values**: 
  - User object
  - Success/error message
- **ORM Operations**:
```python
def register_user(email, password, full_name, address):
    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            address=address,
            balance=0.00
        )
        return user, "Account created successfully"
    except IntegrityError:
        return None, "An account with this email already exists"
```

#### User Authentication
- **Description**: Authenticate a user
- **Input Parameters**: 
  - `email`: User's email address
  - `password`: User's password
- **Return Values**: 
  - User object or None
  - Success/error message
- **ORM Operations**:
```python
def authenticate_user(request, email, password):
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return user, "Login successful"
    return None, "Invalid email or password"
```

#### Update User Profile
- **Description**: Update user information
- **Input Parameters**: 
  - `user_id`: ID of the user
  - `full_name`: User's full name
  - `address`: User's address
  - `password` (optional): New password
- **Return Values**: 
  - Updated User object
  - Success/error message
- **ORM Operations**:
```python
def update_profile(user_id, full_name, address, password=None):
    try:
        user = User.objects.get(id=user_id)
        user.full_name = full_name
        user.address = address
        
        if password:
            user.set_password(password)
            
        user.save()
        return user, "Profile updated successfully"
    except User.DoesNotExist:
        return None, "User not found"
```

#### Update User Balance
- **Description**: Add or withdraw funds from user balance
- **Input Parameters**: 
  - `user_id`: ID of the user
  - `amount`: Amount to add/withdraw
  - `is_addition`: Boolean indicating addition or withdrawal
- **Return Values**: 
  - Updated User object
  - Success/error message
- **ORM Operations**:
```python
def update_balance(user_id, amount, is_addition):
    try:
        user = User.objects.get(id=user_id)
        
        if is_addition:
            user.balance += amount
        else:
            if user.balance >= amount:
                user.balance -= amount
            else:
                return user, "Insufficient balance"
                
        user.save()
        return user, "Balance updated successfully"
    except User.DoesNotExist:
        return None, "User not found"
```

#### Get Purchase History
- **Description**: Retrieve a user's purchase history
- **Input Parameters**: 
  - `user_id`: ID of the user
  - `sort_by` (optional): Field to sort by
  - `filters` (optional): Dictionary of filters
- **Return Values**: 
  - QuerySet of Order objects
- **ORM Operations**:
```python
def get_purchase_history(user_id, sort_by='-created_at', filters=None):
    orders = Order.objects.filter(user_id=user_id)
    
    if filters:
        if 'start_date' in filters:
            orders = orders.filter(created_at__gte=filters['start_date'])
        if 'end_date' in filters:
            orders = orders.filter(created_at__lte=filters['end_date'])
        if 'is_fulfilled' in filters:
            orders = orders.filter(is_fulfilled=filters['is_fulfilled'])
            
    return orders.order_by(sort_by)
```

#### Search Products
- **Description**: Search for products based on criteria
- **Input Parameters**: 
  - `query` (optional): Search keywords
  - `category_id` (optional): Category filter
  - `min_price` (optional): Minimum price
  - `max_price` (optional): Maximum price
  - `sort_by` (optional): Field to sort by
- **Return Values**: 
  - QuerySet of Product objects
- **ORM Operations**:
```python
def search_products(query=None, category_id=None, min_price=None, max_price=None, sort_by='name'):
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    if category_id:
        products = products.filter(category_id=category_id)
        
    if min_price is not None:
        products = products.filter(inventory__price__gte=min_price)
        
    if max_price is not None:
        products = products.filter(inventory__price__lte=max_price)
        
    if sort_by == 'price_asc':
        products = products.order_by('inventory__price')
    elif sort_by == 'price_desc':
        products = products.order_by('-inventory__price')
    else:
        products = products.order_by(sort_by)
        
    return products.distinct()
```

#### Create Product
- **Description**: Create a new product
- **Input Parameters**: 
  - `name`: Product name
  - `description`: Product description
  - `category_id`: Category ID
  - `image`: Product image
  - `created_by_id`: ID of the creator
- **Return Values**: 
  - Product object
  - Success/error message
- **ORM Operations**:
```python
def create_product(name, description, category_id, image, created_by_id):
    try:
        product = Product.objects.create(
            name=name,
            description=description,
            category_id=category_id,
            image=image,
            created_by_id=created_by_id
        )
        return product, "Product created successfully"
    except Exception as e:
        return None, f"Error creating product: {str(e)}"
```

#### Add to Cart
- **Description**: Add a product to the user's cart
- **Input Parameters**: 
  - `user_id`: ID of the user
  - `inventory_id`: ID of the inventory item
  - `quantity`: Quantity to add
- **Return Values**: 
  - CartItem object
  - Success/error message
- **ORM Operations**:
```python
def add_to_cart(user_id, inventory_id, quantity):
    try:
        # Get or create cart
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        
        # Get inventory and check quantity
        inventory = Inventory.objects.get(id=inventory_id)
        if inventory.quantity < quantity:
            return None, "Not enough items in stock"
            
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            inventory=inventory,
            defaults={'quantity': quantity}
        )
        
        # Update quantity if item already exists
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return cart_item, "Item added to cart"
    except Inventory.DoesNotExist:
        return None, "Inventory item not found"
```

#### Place Order
- **Description**: Convert cart to order
- **Input Parameters**: 
  - `user_id`: ID of the user
- **Return Values**: 
  - Order object
  - Success/error message
- **ORM Operations**:
```python
from django.db import transaction

def place_order(user_id):
    try:
        with transaction.atomic():
            # Get user, cart and items
            user = User.objects.select_for_update().get(id=user_id)
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart).select_related('inventory')
            
            if not cart_items.exists():
                return None, "Cart is empty"
                
            # Calculate total amount
            total_amount = sum(item.inventory.price * item.quantity for item in cart_items)
            
            # Check user balance
            if user.balance < total_amount:
                return None, "Insufficient balance"
                
            # Check inventory quantities
            for item in cart_items:
                if item.inventory.quantity < item.quantity:
                    return None, f"Not enough {item.inventory.product.name} in stock"
            
            # Create order
            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                is_fulfilled=False
            )
            
            # Create order items and update inventory
            for cart_item in cart_items:
                inventory = cart_item.inventory
                
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    inventory=inventory,
                    quantity=cart_item.quantity,
                    unit_price=inventory.price,
                    is_fulfilled=False
                )
                
                # Update inventory quantity
                inventory.quantity -= cart_item.quantity
                inventory.save()
                
                # Update seller balance
                seller = inventory.seller
                seller.balance += inventory.price * cart_item.quantity
                seller.save()
            
            # Update buyer balance
            user.balance -= total_amount
            user.save()
            
            # Clear cart
            cart_items.delete()
            
            return order, "Order placed successfully"
    except Exception as e:
        return None, f"Error placing order: {str(e)}"
```

#### Fulfill Order Item
- **Description**: Mark an order item as fulfilled
- **Input Parameters**: 
  - `order_item_id`: ID of the order item
  - `seller_id`: ID of the seller (for verification)
- **Return Values**: 
  - OrderItem object
  - Success/error message
- **ORM Operations**:
```python
from django.utils import timezone

def fulfill_order_item(order_item_id, seller_id):
    try:
        # Get order item and verify seller
        order_item = OrderItem.objects.select_related('inventory', 'order').get(id=order_item_id)
        
        if order_item.inventory.seller_id != seller_id:
            return None, "You are not authorized to fulfill this order item"
            
        if order_item.is_fulfilled:
            return order_item, "Order item already fulfilled"
            
        # Mark as fulfilled
        order_item.is_fulfilled = True
        order_item.fulfilled_at = timezone.now()
        order_item.save()
        
        # Check if all items in the order are fulfilled
        unfulfilled_items = OrderItem.objects.filter(
            order=order_item.order,
            is_fulfilled=False
        ).exists()
        
        if not unfulfilled_items:
            order_item.order.is_fulfilled = True
            order_item.order.save()
            
        return order_item, "Order item fulfilled successfully"
    except OrderItem.DoesNotExist:
        return None, "Order item not found"
```

#### Create Product Review
- **Description**: Submit a review for a product
- **Input Parameters**: 
  - `product_id`: ID of the product
  - `user_id`: ID of the user
  - `rating`: Rating (1-5)
  - `comment`: Review comment
- **Return Values**: 
  - ProductReview object
  - Success/error message
- **ORM Operations**:
```python
def create_product_review(product_id, user_id, rating, comment):
    try:
        # Check if user has already reviewed this product
        review, created = ProductReview.objects.get_or_create(
            product_id=product_id,
            user_id=user_id,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )
        
        # Update existing review
        if not created:
            review.rating = rating
            review.comment = comment
            review.updated_at = timezone.now()
            review.save()
            return review, "Review updated successfully"
            
        return review, "Review submitted successfully"
    except Exception as e:
        return None, f"Error submitting review: {str(e)}"
```

### 5.2 Other Actions

#### Image Upload Handling
- **Description**: Process and save uploaded product images
- **Process**:
  1. Validate file type (jpg, png, etc.)
  2. Validate file size (<= 5MB)
  3. Generate unique filename
  4. Resize image if needed
  5. Save to media directory
  6. Return path for database storage

```python
def handle_uploaded_image(image_file, max_size=5*1024*1024):
    if image_file.size > max_size:
        return None, "Image size exceeds 5MB limit"
        
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image_file.name)[1].lower()
    
    if ext not in valid_extensions:
        return None, "Invalid file type. Supported types: JPG, JPEG, PNG, GIF"
        
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{ext}"
    
    # Define save path
    save_path = os.path.join('products', unique_filename)
    full_path = os.path.join(settings.MEDIA_ROOT, save_path)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Save the file
    with open(full_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)
            
    return save_path, "Image uploaded successfully"
```

#### Email Notifications (Optional)
- **Description**: Send email notifications for events
- **Events**:
  - User registration confirmation
  - Order placement confirmation
  - Order fulfillment notification
  - Balance updates

```python
def send_email_notification(recipient_email, subject, message):
    try:
        send_mail(
            subject,
            message,
            'noreply@miniamazon.com',
            [recipient_email],
            fail_silently=False,
        )
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
```

#### Product Recommendation (Optional)
- **Description**: Generate product recommendations for users
- **Approaches**:
  1. Category-based recommendations
  2. Purchase history analysis
  3. Collaborative filtering

```python
def get_product_recommendations(user_id, limit=5):
    # Get user's purchased products
    purchased_products = OrderItem.objects.filter(
        order__user_id=user_id
    ).values_list('inventory__product_id', flat=True)
    
    # Get categories of purchased products
    categories = Product.objects.filter(
        id__in=purchased_products
    ).values_list('category_id', flat=True).distinct()
    
    # Get recommendations from same categories, excluding already purchased products
    recommended_products = Product.objects.filter(
        category_id__in=categories
    ).exclude(
        id__in=purchased_products
    ).order_by('?')[:limit]
    
    return recommended_products
```

## 6. Design System

### 6.1 Visual Style
- **Color Palette**:
  - Primary: #232F3E (Amazon dark blue)
  - Secondary: #FF9900 (Amazon orange)
  - Accent: #37475A (Dark blue-gray)
  - Background: #FFFFFF (White)
  - Text: #333333 (Dark gray)
  - Success: #007600 (Green)
  - Warning: #FF9900 (Orange)
  - Error: #B12704 (Red)
  - Light Gray: #F3F3F3 (For backgrounds)
  - Border: #DDD (Light gray)

- **Typography**:
  - Primary Font: 'Arial', sans-serif
  - Headings:
    - H1: 24px, bold, #232F3E
    - H2: 20px, bold, #232F3E
    - H3: 18px, bold, #232F3E
    - H4: 16px, bold, #232F3E
  - Body Text: 14px, regular, #333333
  - Small Text: 12px, regular, #666666
  - Links: 14px, #0066C0, no underline (underline on hover)

- **Spacing**:
  - Base Unit: 8px
  - Container Padding: 16px
  - Section Margins: 24px
  - Card Padding: 16px
  - Form Field Spacing: 16px
  - Button Padding: 8px 16px

- **Borders and Shadows**:
  - Border Radius: 4px
  - Card Border: 1px solid #DDD
  - Box Shadow: 0 2px 5px rgba(0,0,0,0.1)
  - Focus Outline: 2px solid #FF9900

### 6.2 Core Components

#### Layout Structure
- **Base Layout**:
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{% block title %}Mini-Amazon{% endblock %}</title>
      <link rel="stylesheet" href="{% static 'css/style.css' %}">
  </head>
  <body>
      <header>
          {% include 'includes/navbar.html' %}
      </header>
      
      <main class="container">
          {% if messages %}
              <div class="messages">
                  {% for message in messages %}
                      <div class="message {{ message.tags }}">{{ message }}</div>
                  {% endfor %}
              </div>
          {% endif %}
          
          {% block content %}{% endblock %}
      </main>
      
      <footer>
          {% include 'includes/footer.html' %}
      </footer>
      
      <script src="{% static 'js/script.js' %}"></script>
      {% block extra_js %}{% endblock %}
  </body>
  </html>
  ```

#### Navigation Patterns
- **Top Navbar**:
  ```html
  <nav class="navbar">
      <div class="navbar-brand">
          <a href="{% url 'home' %}">
              <img src="{% static 'images/logo.png' %}" alt="Mini-Amazon">
          </a>
      </div>
      
      <div class="search-bar">
          <form action="{% url 'products:search' %}" method="GET">
              <input type="text" name="query" placeholder="Search products...">
              <button type="submit" class="btn-search">
                  <i class="fa fa-search"></i>
              </button>
          </form>
      </div>
      
      <div class="navbar-menu">
          <div class="navbar-item">
              <a href="{% url 'carts:view' %}">
                  <i class="fa fa-shopping-cart"></i>
                  <span>Cart</span>
                  {% if cart_count %}
                      <span class="badge">{{ cart_count }}</span>
                  {% endif %}
              </a>
          </div>
          
          {% if user.is_authenticated %}
              <div class="navbar-item dropdown">
                  <a href="#" class="dropdown-toggle">
                      <span>Hello, {{ user.full_name|truncatechars:10 }}</span>
                  </a>
                  <div class="dropdown-menu">
                      <a href="{% url 'users:profile' %}">Your Account</a>
                      <a href="{% url 'users:purchase_history' %}">Your Orders</a>
                      {% if user_is_seller %}
                          <a href="{% url 'sellers:inventory' %}">Your Inventory</a>
                          <a href="{% url 'sellers:fulfillment' %}">Order Fulfillment</a>
                      {% endif %}
                      <a href="{% url 'users:logout' %}">Logout</a>
                  </div>
              </div>
          {% else %}
              <div class="navbar-item">
                  <a href="{% url 'users:login' %}" class="btn-link">Login</a>
                  <a href="{% url 'users:register' %}" class="btn-primary">Register</a>
              </div>
          {% endif %}
      </div>
  </nav>
  ```

- **Category Sidebar**:
  ```html
  <div class="sidebar">
      <h3>Categories</h3>
      <ul class="category-list">
          {% for category in categories %}
              <li {% if current_category == category %}class="active"{% endif %}>
                  <a href="{% url 'products:category' category.id %}">
                      {{ category.name }}
                  </a>
              </li>
          {% endfor %}
      </ul>
  </div>
  ```

#### Shared Components

- **Button Component**:
  ```html
  <button class="btn btn-primary" type="submit">
      {{ button_text }}
  </button>
  ```
  CSS:
  ```css
  .btn {
      padding: 8px 16px;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      border: none;
      transition: background-color 0.3s;
  }
  
  .btn-primary {
      background-color: #FF9900;
      color: #fff;
  }
  
  .btn-primary:hover {
      background-color: #e88e00;
  }
  
  .btn-secondary {
      background-color: #37475A;
      color: #fff;
  }
  
  .btn-secondary:hover {
      background-color: #2c3846;
  }
  ```

- **Product Card Component**:
  ```html
  <div class="product-card">
      <div class="product-image">
          <img src="{{ product.image.url }}" alt="{{ product.name }}">
      </div>
      <div class="product-info">
          <h3 class="product-name">
              <a href="{% url 'products:detail' product.id %}">{{ product.name }}</a>
          </h3>
          <div class="product-price">${{ product.inventory_set.first.price }}</div>
          <div class="product-rating">
              {% include 'includes/rating.html' with rating=product.average_rating %}
              <span class="rating-count">({{ product.review_count }})</span>
          </div>
      </div>
  </div>
  ```

- **Rating Component**:
  ```html
  <div class="rating" data-rating="{{ rating }}">
      {% for i in '12345'|make_list %}
          {% if forloop.counter <= rating %}
              <i class="fa fa-star"></i>
          {% elif forloop.counter <= rating|add:0.5 %}
              <i class="fa fa-star-half-o"></i>
          {% else %}
              <i class="fa fa-star-o"></i>
          {% endif %}
      {% endfor %}
  </div>
  ```

- **Pagination Component**:
  ```html
  {% if is_paginated %}
  <div class="pagination">
      {% if page_obj.has_previous %}
          <a href="?page=1{% if request.GET.query %}&query={{ request.GET.query }}{% endif %}" class="pagination-item">First</a>
          <a href="?page={{ page_obj.previous_page_number }}{% if request.GET.query %}&query={{ request.GET.query }}{% endif %}" class="pagination-item">Previous</a>
      {% endif %}
      
      {% for num in page_obj.paginator.page_range %}
          {% if page_obj.number == num %}
              <span class="pagination-item active">{{ num }}</span>
          {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
              <a href="?page={{ num }}{% if request.GET.query %}&query={{ request.GET.query }}{% endif %}" class="pagination-item">{{ num }}</a>
          {% endif %}
      {% endfor %}
      
      {% if page_obj.has_next %}
          <a href="?page={{ page_obj.next_page_number }}{% if request.GET.query %}&query={{ request.GET.query }}{% endif %}" class="pagination-item">Next</a>
          <a href="?page={{ page_obj.paginator.num_pages }}{% if request.GET.query %}&query={{ request.GET.query }}{% endif %}" class="pagination-item">Last</a>
      {% endif %}
  </div>
  {% endif %}
  ```

- **Alert Component**:
  ```html
  <div class="alert alert-{{ alert_type }}">
      {{ message }}
      <button type="button" class="close" onclick="this.parentElement.style.display='none';">&times;</button>
  </div>
  ```
  CSS:
  ```css
  .alert {
      padding: 12px 16px;
      margin-bottom: 16px;
      border-radius: 4px;
      position: relative;
  }
  
  .alert-success {
      background-color: #dff0d8;
      border: 1px solid #d0e9c6;
      color: #3c763d;
  }
  
  .alert-warning {
      background-color: #fcf8e3;
      border: 1px solid #faf2cc;
      color: #8a6d3b;
  }
  
  .alert-error {
      background-color: #f2dede;
      border: 1px solid #ebcccc;
      color: #a94442;
  }
  
  .alert .close {
      position: absolute;
      top: 10px;
      right: 10px;
      cursor: pointer;
      background: none;
      border: none;
      font-size: 18px;
  }
  ```

## 7. Component Architecture

### 7.1 Server Components

#### Views Implementation

- **Generic Class-Based Views**:
  ```python
  # Example Product List View
  class ProductListView(ListView):
      model = Product
      template_name = 'products/product_list.html'
      context_object_name = 'products'
      paginate_by = 12
      
      def get_queryset(self):
          queryset = super().get_queryset()
          
          # Apply search filter
          query = self.request.GET.get('query')
          if query:
              queryset = queryset.filter(
                  Q(name__icontains=query) | Q(description__icontains=query)
              )
              
          # Apply category filter
          category_id = self.request.GET.get('category')
          if category_id:
              queryset = queryset.filter(category_id=category_id)
              
          # Apply price filters
          min_price = self.request.GET.get('min_price')
          if min_price:
              queryset = queryset.filter(inventory__price__gte=min_price)
              
          max_price = self.request.GET.get('max_price')
          if max_price:
              queryset = queryset.filter(inventory__price__lte=max_price)
              
          # Apply sorting
          sort_by = self.request.GET.get('sort_by', 'name')
          if sort_by == 'price_asc':
              queryset = queryset.order_by('inventory__price')
          elif sort_by == 'price_desc':
              queryset = queryset.order_by('-inventory__price')
          else:
              queryset = queryset.order_by(sort_by)
              
          return queryset.distinct()
          
      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['categories'] = Category.objects.all()
          context['current_query'] = self.request.GET.get('query', '')
          context['current_category'] = self.request.GET.get('category', '')
          context['current_sort'] = self.request.GET.get('sort_by', 'name')
          return context
  ```

- **Form Processing Views**:
  ```python
  # Example Add to Cart View
  class AddToCartView(LoginRequiredMixin, View):
      def post(self, request, *args, **kwargs):
          inventory_id = request.POST.get('inventory_id')
          quantity = int(request.POST.get('quantity', 1))
          
          if quantity <= 0:
              messages.error(request, "Quantity must be greater than zero")
              return redirect('products:detail', pk=request.POST.get('product_id'))
          
          result, message = add_to_cart(request.user.id, inventory_id, quantity)
          
          if result:
              messages.success(request, message)
          else:
              messages.error(request, message)
              
          # Redirect back to product page or referrer
          return redirect(request.META.get('HTTP_REFERER', 'products:list'))
  ```

- **API Views (Optional for AJAX)**:
  ```python
  # Example Cart Update API View
  from django.http import JsonResponse
  
  class CartUpdateAPIView(LoginRequiredMixin, View):
      def post(self, request, *args, **kwargs):
          try:
              cart_item_id = request.POST.get('cart_item_id')
              quantity = int(request.POST.get('quantity'))
              
              cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
              
              if quantity <= 0:
                  cart_item.delete()
                  return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
              
              if cart_item.inventory.quantity < quantity:
                  return JsonResponse({
                      'status': 'error', 
                      'message': f'Only {cart_item.inventory.quantity} items available'
                  })
              
              cart_item.quantity = quantity
              cart_item.save()
              
              # Recalculate cart total
              cart_total = sum(item.inventory.price * item.quantity 
                              for item in CartItem.objects.filter(cart__user=request.user))
              
              return JsonResponse({
                  'status': 'success',
                  'message': 'Cart updated',
                  'item_total': cart_item.inventory.price * quantity,
                  'cart_total': cart_total
              })
          except Exception as e:
              return JsonResponse({'status': 'error', 'message': str(e)})
  ```

### 7.2 Client Components

#### Forms Implementation

- **User Registration Form**:
  ```python
  class UserRegistrationForm(forms.ModelForm):
      password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
      password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
      
      class Meta:
          model = User
          fields = ['email', 'full_name', 'address']
          
      def clean_email(self):
          email = self.cleaned_data.get('email')
          if User.objects.filter(email=email).exists():
              raise forms.ValidationError('An account with this email already exists')
          return email
          
      def clean_password2(self):
          password1 = self.cleaned_data.get('password1')
          password2 = self.cleaned_data.get('password2')
          
          if password1 and password2 and password1 != password2:
              raise forms.ValidationError('Passwords do not match')
          return password2
          
      def save(self, commit=True):
          user = super().save(commit=False)
          user.set_password(self.cleaned_data['password1'])
          if commit:
              user.save()
          return user
  ```

- **Product Form**:
  ```python
  class ProductForm(forms.ModelForm):
      class Meta:
          model = Product
          fields = ['name', 'description', 'category', 'image']
          widgets = {
              'description': forms.Textarea(attrs={'rows': 5}),
          }
          
      def clean_image(self):
          image = self.cleaned_data.get('image')
          if image:
              if image.size > 5 * 1024 * 1024:  # 5MB limit
                  raise forms.ValidationError('Image file too large. Maximum size is 5MB.')
              
              valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
              ext = os.path.splitext(image.name)[1].lower()
              if ext not in valid_extensions:
                  raise forms.ValidationError('Unsupported file extension. Use JPG, JPEG, PNG or GIF.')
          return image
  ```

#### JavaScript Interactions

- **Cart Quantity Update**:
  ```javascript
  document.addEventListener('DOMContentLoaded', function() {
      // Quantity update handlers
      const quantityInputs = document.querySelectorAll('.cart-quantity-input');
      
      quantityInputs.forEach(input => {
          input.addEventListener('change', function() {
              const cartItemId = this.dataset.itemId;
              const quantity = parseInt(this.value);
              
              // Send AJAX request to update cart
              fetch('/cart/update/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/x-www-form-urlencoded',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: `cart_item_id=${cartItemId}&quantity=${quantity}`
              })
              .then(response => response.json())
              .then(data => {
                  if (data.status === 'success') {
                      // Update item total
                      document.getElementById(`item-total-${cartItemId}`).textContent = 
                          `$${data.item_total.toFixed(2)}`;
                      
                      // Update cart total
                      document.getElementById('cart-total').textContent = 
                          `$${data.cart_total.toFixed(2)}`;
                          
                      // Remove row if quantity is zero
                      if (quantity === 0) {
                          document.getElementById(`cart-item-${cartItemId}`).remove();
                      }
                  } else {
                      // Show error message
                      alert(data.message);
                      // Reset input to previous value
                      this.value = this.dataset.originalValue;
                  }
              })
              .catch(error => {
                  console.error('Error:', error);
                  alert('An error occurred. Please try again.');
              });
          });
          
          // Store original value for error handling
          input.dataset.originalValue = input.value;
      });
      
      // Helper function to get CSRF token
      function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              const cookies = document.cookie.split(';');
              for (let i = 0; i < cookies.length; i++) {
                  const cookie = cookies[i].trim();
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
  });
  ```

- **Rating Input**:
  ```javascript
  document.addEventListener('DOMContentLoaded', function() {
      const ratingInput = document.getElementById('rating-input');
      const stars = document.querySelectorAll('.rating-select .star');
      
      if (ratingInput && stars.length) {
          stars.forEach(star => {
              star.addEventListener('click', function() {
                  const value = parseInt(this.dataset.value);
                  ratingInput.value = value;
                  
                  // Update visual state
                  stars.forEach(s => {
                      if (parseInt(s.dataset.value) <= value) {
                          s.classList.add('selected');
                      } else {
                          s.classList.remove('selected');
                      }
                  });
              });
              
              // Hover effects
              star.addEventListener('mouseenter', function() {
                  const value = parseInt(this.dataset.value);
                  stars.forEach(s => {
                      if (parseInt(s.dataset.value) <= value) {
                          s.classList.add('hover');
                      } else {
                          s.classList.remove('hover');
                      }
                  });
              });
          });
          
          // Remove hover effects when leaving the container
          document.querySelector('.rating-select').addEventListener('mouseleave', function() {
              stars.forEach(s => s.classList.remove('hover'));
          });
      }
  });
  ```

## 8. Authentication & Authorization

### Django Authentication Implementation
- Utilize Django's built-in authentication system with a custom User model
- Implement custom login and registration views
- Apply LoginRequiredMixin for protected views

```python
# Custom User Model in users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, address, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            address=address,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, address, password):
        user = self.create_user(
            email=email,
            full_name=full_name,
            address=address,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'address']
    
    def __str__(self):
        return self.email
```

### Protected Routes Configuration
- Use Django's authentication system to protect views
- Implement permission-based access control for seller actions

```python
# Example of a protected view
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class InventoryListView(LoginRequiredMixin, ListView):
    model = Inventory
    template_name = 'sellers/inventory.html'
    context_object_name = 'inventory_items'
    
    def get_queryset(self):
        return Inventory.objects.filter(seller=self.request.user)

# Example of permission-based view (only the product creator can edit)
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update.html'
    
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.created_by
    
    def get_success_url(self):
        return reverse('products:detail', kwargs={'pk': self.object.pk})
```

### Session Management Strategy
- Configure Django's session middleware for handling user sessions
- Implement persistent cart using user's session

```python
# Settings for session management in settings.py
MIDDLEWARE = [
    # ... other middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... other middleware
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400 * 14  # 14 days in seconds
SESSION_COOKIE_SECURE = True  # Use only with HTTPS
SESSION_COOKIE_HTTPONLY = True
```

```python
# Example of session-based cart for non-logged in users
def get_or_create_cart(request):
    if request.user

</implementation_plan>

<existing_code>
{{YOUR_CODE}}
</existing_code>

Implement the whole project for me. 