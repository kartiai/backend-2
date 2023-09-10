from ..db.db import database, User, Website, Product, CartedProd
from app.backend.utils import get_password_hash

async def add_user():
    True
    ### This is for clean up, DELETES all tables ###
    await CartedProd.objects.delete(each=True)
    await Product.objects.delete(each=True)
    await Website.objects.delete(each=True)
    await User.objects.delete(each=True)
    
    u1 = await User.objects.get_or_create(email="andrei@test.com", password=get_password_hash("andrei"))
    b = await User.objects.get_or_create(email="bogdan@test.com", password=get_password_hash("bogdan"))

    ### websites in here ###
    emag = await Website.objects.get_or_create(base_url="https://www.emag.ro/search/", name="emag", domain="www.emag.ro", category="[all]", xpath="""
    {
     "exclude":["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[1]"],
     "include":["//*[@id='card_grid']/div[$ITERATOR$]"],
     "title" : ["//*[@id='card_grid']/div[$ITERATOR$]/div/div/div[3]/div/h2/a/text()"],
     "rating" : ["//*[@id='card_grid']/div[$ITERATOR$]/div/div/div[3]/div/div[1]/a/div[2]/span[1]/text()"],
     "number_of_rating" : ["//*[@id='card_grid']/div[$ITERATOR$]/div/div/div[3]/div/div[1]/a/div[2]/span[3]/text()"],
     "img" : ["//*[@id='card_grid']/div[$ITERATOR$]/div/div/div[3]/a/div[1]/img/@src"],
     "price" : ["//*[@id='card_grid']/div[$ITERATOR$]/div/div/div[4]/div[1]/p[2]/text()"],
     "shipping_price" : [],
     "link_product" : ["//*[@id='card_grid']/div[$ITERATOR$]/div/div/div[3]/a/@href"],
     "currency" : []
     }
    """, country="RO")

    pc_garage = await Website.objects.get_or_create(base_url="https://www.pcgarage.ro/cauta/", name="pc-garage", domain="www.pcgarage.ro", category="[]", xpath="""
       {
     "exclude":[],
     "include":["//*[@id='wrapper_listing_products']/div[$ITERATOR$]"],
     "title" : ["//*[@id='wrapper_listing_products']/div[$ITERATOR$]/div/div[1]/div[2]/div[2]/h2/a/text()"],
     "rating" : [],
     "number_of_rating" : [],
     "img" : ["//*[@id='wrapper_listing_products']/div[$ITERATOR$]/div/div[1]/div[1]/a/picture/img/@src"],
     "price" : ["//*[@id='wrapper_listing_products']/div[$ITERATOR$]/div/div[1]/div[3]/div[1]/div[1]/div[2]/p/text()"],
     "shipping_price" : [],
     "link_product" : ["//*[@id='wrapper_listing_products']/div[$ITERATOR$]/div/div[1]/div[2]/div[2]/h2/a/@href"],
     "currency" : ["RON"]
     }
    """, country="RO")

    amazon  = await Website.objects.get_or_create(base_url="https://www.amazon.com/s?k=", name="amazon", domain="www.amazon.com", category="[all]", xpath="""
   {
     "exclude":["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[6]"],
     "include":["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]"],
     "title" : ["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span/text()"],
     "rating" : ["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]/div/div/div/div/div/div[2]/div/div/div[2]/div/span[1]/span[1]/text()"],
     "number_of_rating" : ["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]/div/div/div/div/div/div[2]/div/div/div[2]/div/span[2]/a/span/text()"],
     "img" : ["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]/div/div/div/div/div/div[1]/div/div[2]/div/span/a/div/img/@src"],
     "price" : ["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/span/span[2]/span[2]/text()"],
     "shipping_price" : [],
     "link_product" : ["//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[$ITERATOR$]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/@href"],
     "currency" : ["DOLAR"]
     }
    """, country="all")

    rombiz = await Website.objects.get_or_create(base_url="https://www.rombiz.ro/", name="rombiz", domain="www.rombiz.ro", category="[all]", xpath="""
     {
     "exclude":[],
     "include":["//*[@id='products-list']/article[$ITERATOR$]"],
     "title" : ["//*[@id='product_box_$ITERATOR$']/div/h2/a/text()"],
     "rating" : [],
     "number_of_rating" : [],
     "img" :   ["//*[@id='product_box_$ITERATOR$']/div/a/img/@src"],
     "price" : ["//*[@id='product_box_$ITERATOR$']/div/div[4]/div[1]/strong/text()"],
     "shipping_price" : [],
     "link_product" : ["//*[@id='product_box_21']/div/h2/a/@href"],
     "currency" : ["RON"]
     }
    """, country="RO")

    ### products emag here ###
    p1 = await Product.objects.get_or_create(website_id=emag[0], product_name="Laptop Lenovo", category="IT", 
                                        image="https://s13emagst.akamaized.net/products/44251/44250473/images/res_2eb9525bba64a13da8e95b10335115f7.jpg",
                                        price="1.598,17")
    p2 = await Product.objects.get_or_create(website_id=emag[0], product_name="Laptop Apple", category="IT", 
                                        image="https://s13emagst.akamaized.net/products/41188/41187834/images/res_4c98933b07a8fd01207cc338b1e2d225.jpg",
                                        price="9.899,99")
    p3 = await Product.objects.get_or_create(website_id=emag[0], product_name="Masina de spalat rufe", category="House", 
                                        image="https://s13emagst.akamaized.net/products/32582/32581589/images/res_7379489e021c4df6b1c82cb9270ddbfd.jpg",
                                        price="2.579,99")


    ## products pc-garage here ###
    p4 = await Product.objects.get_or_create(website_id=pc_garage[0], product_name="Monitor LED ViewSonic", category="IT", 
                                        image="https://4.grgs.ro/images/products/1/8561/2541843/full/gaming-xg2431-238-inch-fhd-ips-05-ms-240-hz-hdr-freesync-blur-busters-approved-20-e44ff332e4f3e411d630dd9b34ccd2f1.jpg",
                                        price="1.499,99")
    p5 = await Product.objects.get_or_create(website_id=pc_garage[0], product_name="Monitor LED GIGABYTE", category="IT", 
                                        image="https://2.grgs.ro/images/products/1/2216/2531995/full/gaming-m28u-ae-28-inch-uhd-ips-1-ms-144-hz-usb-c-hdr-freesync-premium-pro-ac94fc1a5d9eb096ec28bc264d821713.jpg",
                                        price="3.757,98")
                                        
    ### add products in users carts here ###
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p1[0])
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p2[0])
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p3[0])
    await CartedProd.objects.get_or_create(user_id=r[0], product_id=p4[0])
