FCC Political Ads
==================

FCC Political Ads tracks political ad buy documents across television stations, and powers PoliticalAdSleuth.com

Most data comes directly from the FCC's RSS feed, but this code also contains functionality to (i) scrape station websites in case the RSS feed goes down temporarily and (ii) accept manual uploads/entry of documents and metadata by volunteers.

This code was originally written prior to 2012 and 2014 developments in which the FCC ordered affiliates of the top broadcast networks to begin posting their political ad files online. As such, volunteer document entry was key to how the project was conceptualized at the time, but generates a significantly smaller share of the data now. This shift in the primary purpose of the code warrants an overall refactor at such point that additional major pieces of functionality are being considered.




Setting up for local development
---------------------------

**Installing packages**

These instructions assume that you'll be developing inside a virtual environment.

1. Once you've cloned this repository, navigate to the top level of `fcc_political_ads`. You should see a `requirements.txt` file here.

2. Create and activate your virtual environment, and install packages by running:

     ```pip install -r requirements.txt```

3. Note that if you don't already have Mercurial installed on your system, you'll see errors related to the hg command when you run the command above, and your installations will not begin. To address this, first run this command on its own:

     ```pip install mercurial```

     and then run

     ```pip install -r requirements.txt```  
  
  
**Configuring local settings** 

4. Navigate to `fcc_politicalads/fcc_adtracker/fcc_adtracker`
You should see both a `settings.py` file and a `local_settings.py.example` file.

5. Create a copy of `local_settings.py.example` and name it `local_settings.py`.
This code is set up such that settings.py pulls from `local_settings.py`, and `local_settings.py` is excluded from version control. The rest of the steps in this section are for changes you shold make to `local_settings.py`.

6. Finish defining the database backend by completing the line for the `'ENGINE'` field:

    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',                      # Or path to database file if using sqlite3.
            ....
        }
    }
    ```

    So, for example, the following is fine for development in sqlite3: 
        'ENGINE': 'django.db.backends.sqlite3',

7. Change the `SECRET_KEY` to any string you'd like, and share this with no one.

8. Fill in `DOCUMENTS_PATH` in the DocumentCloud section as follows:

    ```DOCUMENTS_PATH = os.path.join(MEDIA_ROOT, 'documents')```

9. You'll need to add something to the `STATIC_URL`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` fields to avoid authorization handler errors.


**Database setup and synchronization** 

Forthcoming.



App structure and other context clues for developers
----------------------------------------------------

Forthcoming.