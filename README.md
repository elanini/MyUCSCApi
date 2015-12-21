# Unofficial MyUCSC API

This is an incomplete unofficial API for UCSC's MyUCSC student portal. It works by automating actions in a headless browser. I am not liable for messing up your enrollment.

Current features:
  - login
  - add to shopping cart
  - enroll
  - convert class name to ID
  - convert ID to class name
 
### USAGE
PhantomJS and Selenium are required. Example usage: 
```py
import myucsc
myucsc.login('username', 'password')
myucsc.add_to_shopping_cart(40933, 0, 40934, False)
myucsc.enroll(40933)
```


### TODO
  - safety checks
  - drop
  - swap
  - edit
  - get transcript?
  - other