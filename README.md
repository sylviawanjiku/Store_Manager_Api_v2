# StoreManager_Api_v2

Store Manager is an app that allows users to control sales and inventory.
The store manager app has two type of users store attendant and store owner(admin).
Each of the two users have their indivindual roles to play but in this case what the store attendant can do the admin can also do.

### Running the application
1. clone this repository
2. Navigate to the project directory
3. Activate the virtual environment `$ source .env`
4. Install dependencies needed for the project to run `$ pip install -r requirements.txt`
5. install flask `$ pip install flask`
6. Run the application `$flask run`
7. To test the test `$ pytest`

### The store attendant can perform the following:

1. Login to the app
2. View all products 
3. View a single product
4. Make a sale 
5. View a personal sales record

### The store owner can perform the following:
1. Login to the app
2. register a new user
3. add a product to inventory
4. view sales record
5. view a specific sales record with respect to te user who made the sale

### The API Endpoints

1. post-register user   http://127.0.0.1:5000/api/v2/signup   
2. post-login user  http://127.0.0.1:5000/api/v2/login   
3. post-create products     http://127.0.0.1:5000/api/v2/products   
4. post-create sale record  http://127.0.0.1:5000/api/v2/sales 
5. get-fetch products   http://127.0.0.1:5000/api/v2/products
6. get-fetch single product     http://127.0.0.1:5000/api/v2/products/product_id
7. delete-delete single product http://127.0.0.1:5000/api/v2/products/product_id


### Testing the app

The endpoints above can be tested using  `Postman.`

