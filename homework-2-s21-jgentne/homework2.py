def histogram(data, n, b, h):
    # data is a list
    # n is an integer
    # b and h are floats
    
    # Write your code here
    if n <= 0 or h < 1:
        return 
    else:
        w = (h-b)/n
        hist = [0]*n

        for i in range(n):
            for j in data:
                if (b + i * w) <= j < (b + (i+1) * w):
                    hist[i] += 1
                    
        return hist

    # return the variable storing the histogram
    # Output should be a list

pass


def addressbook(name_to_phone, name_to_address):
    #name_to_phone and name_to_address are both dictionaries

    # Write your code here
    address_to_all = {}
    names = name_to_address.keys()

    for x in names:
        if(name_to_address[x] in address_to_all):

            nameList = address_to_all[name_to_address[x]][0]
            nameList.append(x)
            name_to_dictionary = name_to_phone[x]
            phone_to_dictionary = address_to_all[name_to_address[x]][1]

            if (name_to_dictionary != phone_to_dictionary):

                first_name = address_to_all[name_to_address[x]][0][0]
                print('Warning: {} has a different number for {} than {}. Using the number for {}.' .format(x, name_to_address[x], first_name, first_name))
            
        else:

            address_to_all.update({name_to_address[x]: ([x], name_to_phone[x])})

    # return the variable storing address_to_all
    # Output should be a dictionary

    return(address_to_all)
    
pass