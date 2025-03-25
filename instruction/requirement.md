<?xml version="1.0" encoding="UTF-8"?>
<project>
    <title>Miniature Amazon Website</title>
    <description>
        A website where sellers create product listings and manage inventory, users browse and purchase products using virtual currency, and feedback is provided through reviews and messaging.
    </description>
    <team>
        <member role="Users Guru">Account / Purchases</member>
        <member role="Products Guru">Products</member>
        <member role="Carts Guru">Cart / Order</member>
        <member role="Sellers Guru">Inventory / Order Fulfillment</member>
        <member role="Social Guru">Feedback / Messaging</member>
    </team>
    <collaboration_note>
        Team members must collaborate on database design, website design, code integration, and testing.
    </collaboration_note>

    <!-- Module 1: Account / Purchases -->
    <module name="AccountPurchases">
        <basic_requirements>
            <feature>
                <description>New user registration and existing user login using email and password.</description>
            </feature>
            <feature>
                <description>User account with system-assigned ID, email (unique), full name, address, and password (editable except ID).</description>
            </feature>
            <feature>
                <description>Account balance starts at $0; users can top up or withdraw (no real payment mechanism needed).</description>
            </feature>
            <feature>
                <description>Browse purchase history sorted by reverse chronological order, showing summary (total amount, number of items, fulfillment status) and linking to detailed order page.</description>
            </feature>
            <feature>
                <description>Public user view showing ID, name, and summary info; if a seller, include email, address, and seller reviews.</description>
            </feature>
        </basic_requirements>
        <additional_features>
            <feature>
                <description>Search/filter purchase history by item, seller, date, etc.</description>
            </feature>
            <feature>
                <description>Visualize balance history, spending amounts, and purchases by category.</description>
            </feature>
        </additional_features>
    </module>

    <!-- Module 2: Products -->
    <module name="Products">
        <basic_requirements>
            <feature>
                <description>Predefined product categories; each product has a name, description, image, and price.</description>
            </feature>
            <feature>
                <description>Browse and search/filter products by category, keywords in name/description, and sort by price; show summary (image, name, average rating) with link to detailed page.</description>
            </feature>
            <feature>
                <description>Detailed product page with all details, list of sellers with stock quantities, interface to add to cart, and product reviews.</description>
            </feature>
            <feature>
                <description>Users can create and edit products for sale.</description>
            </feature>
        </basic_requirements>
        <additional_features>
            <feature>
                <description>Enhance filtering/sorting by review rating, total sales, price, or availability of highly rated sellers.</description>
            </feature>
            <feature>
                <description>Implement hierarchical labels or tags for products; define creation/maintenance process.</description>
            </feature>
            <feature>
                <description>Standardize products across sellers; decide if different prices are allowed.</description>
            </feature>
        </additional_features>
    </module>

    <!-- Module 3: Cart / Order -->
    <module name="CartOrder">
        <basic_requirements>
            <feature>
                <description>User cart with line items (product, seller, quantity); detailed cart page shows items, total price, and options to modify or submit as an order.</description>
            </feature>
            <feature>
                <description>Order submission checks inventory and balance, updates them at submission time, empties cart; buyer’s balance decrements, sellers’ balances/inventories update.</description>
            </feature>
            <feature>
                <description>Persistent cart contents across sessions.</description>
            </feature>
            <feature>
                <description>Detailed order page shows final prices, line item fulfillment status; order marked fulfilled when all items are fulfilled, unchangeable post-submission.</description>
            </feature>
        </basic_requirements>
        <additional_features>
            <feature>
                <description>Divide cart into “in cart” and “saved for later” with options to move items.</description>
            </feature>
            <feature>
                <description>Implement promotional coupon codes for discounts on items or cart.</description>
            </feature>
        </additional_features>
    </module>

    <!-- Module 4: Inventory / Order Fulfillment -->
    <module name="InventoryOrderFulfillment">
        <basic_requirements>
            <feature>
                <description>Seller inventory page lists products, allows adding products, and editing/removing quantities.</description>
            </feature>
            <feature>
                <description>Browse/search order fulfillment history sorted by reverse chronological order; show buyer info, order details, and fulfillment status; allow marking items as fulfilled (no inventory update post-submission).</description>
            </feature>
        </basic_requirements>
        <additional_features>
            <feature>
                <description>Add visualizations/analytics for inventory and order trends.</description>
            </feature>
            <feature>
                <description>Add buyer analytics (ratings, messages) for sellers.</description>
            </feature>
        </additional_features>
    </module>

    <!-- Module 5: Feedback / Messaging -->
    <module name="FeedbackMessaging">
        <basic_requirements>
            <feature>
                <description>Single product rating/review per user, editable/removable, submitted via product page.</description>
            </feature>
            <feature>
                <description>Single seller rating/review per user (post-order), editable/removable, submitted via order page or seller public view.</description>
            </feature>
            <feature>
                <description>List all user-authored ratings/reviews, sorted by reverse chronological order, editable via account view.</description>
            </feature>
            <feature>
                <description>Summary ratings (average, count) and sorted review lists for products and sellers.</description>
            </feature>
        </basic_requirements>
        <additional_features>
            <feature>
                <description>Private message threads between buyer and seller per order, shown in order views, chronological, non-editable.</description>
            </feature>
            <feature>
                <description>Upvote functionality for reviews; top 3 helpful reviews shown first, then most recent.</description>
            </feature>
            <feature>
                <description>Allow limited image uploads in reviews, easily viewable.</description>
            </feature>
        </additional_features>
    </module>

    <!-- Integration Section -->
    <integration name="PuttingThemTogether">
        <basic_requirements>
            <feature>
                <description>Integrate all modules into coherent frontend and backend designs, ensuring smooth user task flows and seamless transitions.</description>
            </feature>
        </basic_requirements>
        <additional_features>
            <feature>
                <description>Recommend products based on purchase history and reviews, shown in product views, cart, or history.</description>
            </feature>
            <feature>
                <description>Design process for shipping confirmation, receipt verification, and dispute resolution; rethink balance update timing.</description>
            </feature>
        </additional_features>
    </integration>
</project>