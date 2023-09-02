Following steps need to be taken sequence wise to run code:

1.Keep directory structure the same as kept in sent rar file.

2.First of all run the survey_db_initializer.sql file which will initialize database named survey_db with tables of user,survey and admin. It will also put default credentials of admin (wirtten below) in admin table.

3.Open app.py file and see imports in it. If you have any error on some import i.e. not downloaded that imported library or something , then open terminal like cmd/powershell and write "pip install libraryname".For example, if you have error on flask_session means its not downloaded.Then open cmd/powershell and write "pip install flask_session".

4.After above steps , you are good to go.Just run the app.py file and follow website link. Afterwards, the website is made to be used easily. Cheers!


Important points:

1.Admin Credentials: 
  email:  admin@gmail.com
  pasword: pass

2.User must fill in answers to every question to submit form without errors.

3.One email can only be assigned to one user. If more than one sign up with same email is tried, you will see error.

4.One user can only fill one survey form.If he tries to fill it again, an error will be encountered saying something like duplicate key:PRIMARY().