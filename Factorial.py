#
# 
# author:

# f(n) = n*f(n-1)

def factorial(n): # - док стринг, можем тестировать 
    """
       This is function calculate factorial of int. 
    >>> factorial(0)
    1
    >>> factorial(5)
    120
    >>> [factorial(i) for i in range(6)]
    [1, 1, 2, 6, 24, 120]
    """
    if n < 0:
        raise ValueError('Argument n must be nonnegative') # raise - создать переменную типа ValueError, которая остановит функцию 
    elif not isinstance(n, int): # - проверяет тип 
        raise ValueError('Argument n must be int')
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
