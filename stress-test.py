
from locust import task, TaskSet

class SellerTaskSet(TaskSet):
    @task(10)
    def read_partners(self):
        cust_model = self.client.get_model('res.partner')
        cust_ids = cust_model.search([])
        prtns = cust_model.read(cust_ids)
        
    @task(5)
    def read_products(self):
        prod_model = self.client.get_model('product.product')
        ids = prod_model.search([])
        prods = prod_model.read(ids)
        
    @task(20)
    def create_so(self):
        prod_model = self.client.get_model('product.product')
        cust_model = self.client.get_model('res.partner')
        so_model = self.client.get_model('sale.order')
        
        cust_id = cust_model.search([('name', 'ilike', 'fletch')])[0]
        prod_ids = prod_model.search([('name', 'ilike', 'ipad')])
        
        order_id = so_model.create({
            'partner_id': cust_id,
            'order_line': [(0,0,{'product_id': prod_ids[0], 
                                 'product_uom_qty':1}),
                           (0,0,{'product_id': prod_ids[1], 
                                 'product_uom_qty':2}),
                          ],
            
        })
        so_model.action_button_confirm([order_id,])
from OdooLocust import OdooLocust
from SellerTaskSet import SellerTaskSet

class Seller(OdooLocust):
    host = "not going to leak this"
    database = "not this either"
    min_wait = 100
    max_wait = 1000
    weight = 3
    
    task_set = SellerTaskSet
