# Location Information

For Quinton to be able to give you information about the time or weather, it needs to be able to
access your location and timezone data. As of right now, it isn't automatically set for you (sorry),
so you'll have to do it yourself (unless you plan on disabling this functionality).

## Getting Location Data

Location data is what allows Quinton to give the weather forecast. To do this, it uses your city name
and the ISO 3166 2-character country code. By default, Quinton detects the weather for Ellicott City in the United States,
but you can change it by following these steps:

1. Go to [openweathermap.org](openweathermap.org)

2. Search for your city name. There may be multiple cities with the same name, so try to find the one for your country.
   If this is the case, try them all until you find the right one.

3. Select the city

4. You should see text in the form _city name_, _country code_ (e.g., Los Angeles, US)

5. Navigate to the `config.yaml` file in the `../config` directory

6. Under `location_pref`, set `city` the the city name and `country` to the country code.

### If you want to find the country code a different way

1. Go to the [iso.org Online Browsing Platform](iso.org/obp/ui/#home)

2. Click the bubble above the search bar labeled "Country codes"

3. Search for your country

4. The code will be listed under the "Alpha-2 code" heading in the table. Note that you may get multiple countries
   in the search results, so you might have to do some looking for your country/country code.

Enjoy your weather forecast!

## Getting Timezone Data

Timezone data helps Quinton get the time correct. This is very important, and not just for asking about the time.
For example, Quinton uses the time to do things like timestamp history data and error logs. Quinton uses [Stuart Bishop](github.com/stub42)'s
[pytz](github.com/stub42/pytz) library for handling timezones, which requires the timezone name to be from the
[IANA Timezone Database](iana.org/time-zones).

By default, the timezone is set to Eastern Time (United States), but you can change it by following these steps:

1. Open up a terminal and run the command `python3.8 tzcodes.py`
   * Note that `tzcodes.py` **requires Python 3.8+**, so you need to have
     a Python version that meets this requirement. If you have, say,
     Python 3.9, use the command that is for **your version**.
   * You'll likely already have this, because 3.8+ is required to run the software

2. Follow any prompts

3. Set the `timezone` variable in `../config/config.yaml` to the
   **exact** name you found in the list. **This parameter is case sensitive!**

For more information about pytz timezones and available timezone lists, see the pytz library's
[README](github.com/stub42/pytz/blob/master/src/README.rst) on GitHub

Enjoy the correct answer when you ask Quinton for the time!
