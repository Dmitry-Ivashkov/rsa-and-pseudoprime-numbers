import math
import random

r_range = 2 ** 50
l_range = 2 ** 47


def luk_test(namber, random_sample):
    out_bool = False
    a_out = 0
    for a in range(2, math.ceil(math.log2(namber))):
        flag = False
        if 1 == fast_pow_mod(a, namber - 1, namber):
            for i in random_sample:
                if 1 != fast_pow_mod(a, (namber - 1) // i, namber):
                    a_out = a
                    out_bool = True
                    flag = True
                    break
        if flag == True:
            break
    return (out_bool, a_out)


def one_gen_primes():
    array = list(
        [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127])
    k = 0
    while (k < 5) or (k > 20):
        k = math.ceil(random.random() * len(array))
    random_sample = random.sample(array, k)
    random_sample.append(2)
    namber = 1
    for i in random_sample:
        namber = namber * i
    while (math.log2(namber) < math.log2(l_range)):
        namber = namber * random.choice(random_sample)
    namber = namber + 1
    test = luk_test(namber, random_sample)
    return (namber, random_sample, test[0], test[1])


def gen_primes():
    one = one_gen_primes()
    while one[2] == False:
        one = one_gen_primes()
    return (one[0], one[1], one[3])


def fast_pow_mod(base, degre, module):
    degre = bin(degre)[2:]
    r = 1
    for i in range(len(degre)):
        r = (r ** 2) % module
        r = (r * (base ** int(degre[i]))) % module
    return r


def my_big_random(n):
    return random.getrandbits(math.ceil(math.log2(n)))


def my_big_random_nechotniy(a, b):
    c = my_big_random(b)
    while (c < a) or (c % 2 == 0):
        c = my_big_random(b)
    return c


def do_s_d(n):
    n = n - 1
    s = 0
    while n % 2 == 0:
        s += 1
        n = n // 2
    return s, n


def test_rabin(n):
    out_bool = True
    count = 0
    s, d = do_s_d(n)
    # print(s, d)
    while (out_bool == True) and (count <= math.log2(n)):
        count += 1
        a = my_big_random_nechotniy(2, n - 1)
        # print('a:',a)
        ad = fast_pow_mod(a, d, n)
        # print('ad1:',ad)
        if (ad == 1) or (ad == n - 1):
            continue
        i = 0
        while (out_bool == True) and (i < s):
            i += 1
            ad = fast_pow_mod(ad, 2, n)
            # print('ad:',ad)
            if ad == n - 1:
                break
        # print(i)
        if i == s:
            out_bool = False
    return out_bool


def gen_pseudoprime():
    n = my_big_random_nechotniy(l_range, r_range)
    # test = test_rabin(33)
    # test = test_rabin(gen_primes()[0])
    test = test_rabin(n)
    # print('test:',test)
    while test == False:
        # print(n)
        n = my_big_random_nechotniy(l_range, r_range)
        test = test_rabin(n)
    return n


def evclid(a, n):
    if 0 == n:
        return (1, 0, a)
    y, x, g = evclid(n, a % n)
    return (x, y - (a // n) * x, g)


def obrat(a, n):
    ob = evclid(a, n)[0]
    if ob < 0:
        ob += n
    return ob


def rsa_gen_keys():
    p = gen_pseudoprime()
    q = gen_pseudoprime()
    fi = (q - 1) * (p - 1)
    e = my_big_random_nechotniy(15, fi)
    while math.gcd(e, fi) != 1:
        e = my_big_random_nechotniy(15, fi)
    d = obrat(e, fi)
    return p * q, p, q, e, d


def rsa_encrypt(n, e, t):
    return fast_pow_mod(t, e, n)


def rsa_decrypt(n, d, s):
    return fast_pow_mod(s, d, n)


def prime_factorization_pollard(n, cutoff):
    a = my_big_random(n)
    p = 1
    for i in range(cutoff):
        b = fast_pow_mod(a, math.factorial(i), n) - 1
        g = math.gcd(b, n)
        if (g != 1) and (g != n):
            p = g
            break
    return p


print(gen_pseudoprime())