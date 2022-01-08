def function(ctx, view):
    ctx = 'Ä'
    view = 'Ä'
    return ctx, view


print(type(function('a', 'b')), function('a', 'b'))

