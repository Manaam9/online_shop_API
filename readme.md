# online_shop_API

This project realize online shop API for posting plenty of products and reviews. 
For correct start of application it's required to install and activate pipenv and apply all migrations. 
Also it is required to create superuser and other users to access db. Make sure everything is done do deploy on production. 
Technical description of the project you can see below:

/api/v1/goods/ (POST) - create product in online shop. Format of request: application/json. Example of request: 
{ "Authorization":"Base dXNlcjp1c2Vy" "title": "Cheese"Russian"", "description": "Very delicious cheese, almost like Italian.", "price": 100 } 

Limitations:

    You can access only if you user has is_staff flag.
    All fields are required.
    title - not empty string, not longer than 64 symbols.
    description - not empty string, not longer than 1024 symbols.
    price - not empty string ( that can be converted to int) or int, values from 1 to 1000000 
    Possible answers:
        201 - product successfully saved Example of answer: {"id": 112}
        400 - request didn't pass validation

 /api/v1/goods/:id/reviews/ (POST) - create review to product, where :id - id of product. 
Format of request: application/json Example of request: { "text": "Best. Cheese. Ever.", "grade": 9 } 

Limitations:

    All fields are required.
    text - not empty string, not longer than 1024 symbols.
    grade - not empty string ( that can be converted to int type ) or, values from 1 to 10 
    Possible answers:
        201 - review successfully saved Example of answer: {"id": 95}
        400 - request didn't pass validation
        404 - There is no product with that id

/api/v1/goods/:id/ (GET) - get product information, including the latest 5 reviews. Format of request: application/json 

Limitations:

    If there's more than 5 reviews - return 5 latest. Sort by id of review.
    If there's 5 reviews - return all. 
    Possible answers:
        200 - OK Example of request: {
            "id": 112, "title": "Cheese 'Russian'", 
            "description": "Very delicious cheese.", 
            "price": 100, 
            "reviews": [{ "id": 95, "text": "Best. Cheese. Ever.", "grade": 9 }]
            }
        404 - There is no product with that id.
