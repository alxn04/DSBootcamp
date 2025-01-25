def data_types():
      a = 2
      b = "string"
      c = 3.5
      d = True
      e = [1,2,3,4]
      f = {'x' : [1,2]}
      g = (1,2,3)
      m = set(b)
      list_types = [type(x).__name__ for x in [a, b, c, d, e, f, g, m]]
      print(list_types)

def main():
     try:
         data_types()
     except Exception as e:
         print(f"Error in data_types(): {e}")

if __name__ == '__main__':
    main()