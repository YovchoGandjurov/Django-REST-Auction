# Django REST Framework Auction Project


### Summary:
This repo shows the created Django REST Auction. The goals of the project creation are to show everything learned about REST framework from <a href="https://softuni.bg/trainings/2150/django-web-development-march-2019" target="_blank">**Django Web Development**</a> course organized by **Software University** and to represent and defend the project as a final examination.

## About the project
REST project that serves to create and store auctions. There is a simple login/register functionality for users and full CRUD for their accounts and auctions. The authenticated user can bid for one or more auctions and when the end date added by the creator is reached the auction closes and the winner is the last bidder.

## Django REST - project Assignment
<b>Mandatory requirements:</b>
 - The project must have login/register functionality
 - Must have public part (A part of the website, which is accessible to everyone – un/authenticated users, admins)
 - Must have private part (accessible only to authenticated user and to admins)
 - Admin part (accessible only to admins)
 - Unauthenticated users (public part) have only ‘get’ permissions
 - Authenticated users (private part) – have full CRUD for all of their created content + PATCH
 - Admin part – Admin/s has/ve full CRUD for all products on the website + PATCH
 - Reusable serializers of the model – one model many serializers
 - Nested serializares
 - Usage of APIViews
 - Class-based views
 - Different relationships (Many-to-many, one-to-many, many-to-one) presented

<b>Bonuses:</b>
 - Testing (unit testing)
 - Extended Django user
 - Anything that is not described in the assignment is a bonus if it has some practical use. 
 - Documentation/ Swagger
 - Github/Gitlab – at least 3 commits and at least 3 days of history + README

## Used to build the REST project

 <b>1. Account App</b>

- <b>Login functionality from rest_framework.urls</b>
- <b>Custom register functionality</b> - Extended Django User using field 'sourse' to relate with defaul User fields. Added 'first_last_name' field(read only) that combines the first and last name. Validate username with 'Field-level validation' to be unique. Overriding 'create' and 'update' methods in serializers to create/update the both User and Profile(extended user). Full CRUD for account owner.
- <b>Default and custom permissions</b> - create account only for unauthorized users or admins/superusers; list accounts only for admin users; Retrieve, Update and Delete only for authorized users owners or admins/superusers.
- <b>Tests</b> - register account with dummy data and check if saved in db; The password should not be in response and in planetext. Login user, edit profile and test that can not see foreign accounts. 

 <b>2. Auction App</b>

- <b>Models</b> - auction and category models with needed fields. Used ForeignKey reletion for 'category', 'owner' and 'winner' and ManyToManyField reletion to Profile for 'participants'.
- <b>Serializers</b> - <b>Create Auction</b> - Overriding 'create' method to create аn auction, add the current user as owner and update current price to be equal to the initial price. Validate closing_date with 'Field-level validation' to be in the future; <b>List Auction</b> - Overriding fields 'owner', 'winner' and 'participants' with 'MethodField()' to be represend as nested from the Profile Serializer; <b>Update Auction</b>; <b>Bid Auction</b> - partial update; <b>Category</b> - using for full CRUD.
- <b>Views and Permissions</b> - <b>Create Auction</b> - only for authenticated users; <b>List and Create Auction</b> - List for all users and Create only for admins. Using 'get_serializer_class' to get different serializer for list and create. Using django ordering and filtering for 'current_price' and 'closing_date' fields. Overriding 'queryset' to check auction closing_date and close the auction if the date is in the past. Also, show all auction for the admins and only opened for all other users; <b>List Auction on the current user</b> - only for authenticated users; <b>Retrieve, Update and Delete</b> -  Only for owners or admins. Using 'get_serializer_class' to get different serializer for list and update. Owners can not delete if 'number_of_bids' field is different from zero. <b>Bid Auction</b> - list for all users and bid only for authenticated. Using 'get_serializer_class' to get different serializer for list and patch. Using 'partial_update' from ModelViewSet to do a bid with patch. Along with this method changes the 'number_of_bids', 'current_price', 'winner' and 'participants'; <b>List and Create Category</b> - List for all and Create for admin users; <b>Retrieve, Update and Delete</b> - Only for admins.
- <b>Tests</b> - Create auction; Unauthenticated user create auction; Create auction with past date; User edit own auction; User delete own auction; Make bid less than step or with string; Unauthenticated user can not bid; Post category;

 <b>3. Data Base and Settings</b>

- The project used PostgreSQL data base.
- Used 'dotenv' package to store sensitive information in .env file.
- Used 'rest_framework_swagger' to represend project schema.
- Added django REST pagination.

# Certificate
<p align="center"><img src="CERTIFICATE - Django Web Development.png" alt="CERTIFICATE" width="540"></p>
