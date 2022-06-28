e = 65537
n1 = 6490575414546753422169557924726633698938840342804007877593140124713933084247239272632050468659186332284597365791524523203890501075477199471733446503331287392773585633905281136028592442460859381818517915584152977506750156812875265542004792964515179303151752533661952619290383021701963596253894613400006395933540184308383205582620641667831066786941489460633668241024642868786169958309890455670637684750726393954761545971579402229970767454083426068165630397383861060884335031186141866257202083321618111563513626855089058455000733251707282966148763783562830207713984490916122334630807846682310867739481868099531604199361
c1 = 1371759048149611040770011921418215274402106876461640344401671404760028350471019509755594539076613816766603306047375261901377330195783332158141855247009473212134079930634738546463366062005611533899217760683884243552925137820869416006162234259026748413289532952661691110428194702340622114401978375464352186350704087241652696132238723998349724100265841522875869638348652264210710788722315420766378666865380442669403058098363185242109346451512352300814495546093790945666900753896675597726653142708523272375106881144319062453373966096109696111579547829616782570851839672780482070134871669403035987583702072195847608957359
n2 = 13908131502186888224364262080833432482112861581791111042080173649970166026500874345460017841288071475736405123781852190183413966703850124472840235945014409259347227565898256371761534183506997838619648382565719683809192690932704492409765399588791914002222178163703645294336900346832278341843927619793929067019394635129701010101745788281692696408082738016096835941283027842912901321468805256876430916029359283952631637587185030521085502993312596951304076920403362682120118569535468210808087497348286199962361033672950036309555605765599177178688696972244879328867379830135765957335666748015324124120372593527528004246553
c2 = 13328797044862662040031336230712258541783627901094587775876771299742074083680668896746399241086714119830688395349669302694505303651730534145158997674920873640772428508628089236079960707540568179840256034900463343673430411467530242996605459278602091508195203902676963982374006581722502811925835672334973207193807537155840718929964442943000099917015241745382770009470964464459371708987908791454965936419120107641347519737033356242627992230599067761853501335939840610231285729885833878366987477004347128006121486442078361960058397114501698227903288899815398102056944015302283951908059548073442330608775519166795679207096

def sqrt(n):
    l = 1
    r = n
    while l<r:
        m = (l+r)//2
        if m*m == n:
            return m
        if m*m < n:
            l = m+1
        if m*m > n:
            r = m-1
    return l

def close_primes(n):
    for p in range(sqrt(n), n):
        q = n // p
        if p*q == n:
            return p, q

p1 = (sqrt(sqrt(n1)))
assert p1 ** 4 == n1
print(f"{p1 = }")

f1 = (p1-1) * p1**3
d1 = pow(e, -1, f1)
m1 = pow(c1, d1, n1)


p2, q2 = close_primes(n2)
assert p2 * q2 == n2
print(f"{p2 = }")
print(f"{q2 = }")

f2 = (p2-1) * (q2-1)
d2 = pow(e, -1, f2)
m2 = pow(c2, d2, n2)


from Crypto.Util.number import long_to_bytes

print(long_to_bytes(m1)+long_to_bytes(m2))
