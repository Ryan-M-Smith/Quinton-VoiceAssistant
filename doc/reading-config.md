# How I set up Quinton's configuration file reader

When reading Quinton's configuration files in `../src/config.py`, the `setattr()`
method is used to save time when setting corresponding class variables from
`../data/config/config.yaml`. To set each variable by hand would have been time
consuming and would lead to hard-to-understand code, especially when I had to deal
with dictionaries nested inside of arrays. So, instead of checking for each variable
and setting it through a bunch of if-elif-else statements, I was able to simply
iterate through the YAML document and set each variable by using the class name, the
name of the variable (same as the key in YAML), and the value, which was taken from
the config file.

---

Here is what the code looks like, with and without using `setattr()`.

**Without:**

```python
for key, value in a_dict.items():
  if key == "username":
    self.username = value
  elif ...: # Another "key == name" statement
    # Set the variable
```

**With:**

```python
for key, value in a_dict.items():
  setattr(cls, key, value) # key would equal "username"
```
