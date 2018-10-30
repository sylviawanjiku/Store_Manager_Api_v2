class Product():
    products = []
    def __init__(self,product_id,product_name,brand,quantity,price,avail_stock,min_stock,uom,category):
        self.product_id = product_id
        self.product_name = product_name
        self.brand = brand
        self.quantity =quantity
        self.price = price
        self.avail_stock = avail_stock
        self.min_stock = min_stock
        self.uom = uom
        self.category = category
        
    def post_product(self):      
        product_data = dict(
            id =  len(Product.products),
            product_id = self.product_id,
            product_name= self.product_name,
            brand = self.brand,
            quantity =self.quantity,
            price = self.price,
            avail_stock = self.avail_stock,
            min_stock = self.min_stock,
            uom = self.uom,
            category = self.category        
           )
        self.products.append(product_data)

        return product_data

        
    def get_products(self):
        # fetch all products
        return  Product.products
        
    def get_single_product(self,product_id):
        single_product= [product for product in Product.products if int(product['id']) == int(product_id)]
        if single_product:
            return single_product 

    
      
