# a bit slow, no time for sort...

from collections import defaultdict as d
import heapq as hq
import sys


sys.setrecursionlimit(100_000)                                                        # 36 366 98 989 98989 LL


PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
          101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
          211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
          307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
          401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
          503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
          601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
          701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
          809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
          907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
          ]


def divisors(n: int) -> list[int]:  # 36 366 98 989 98989 LL
    prime_factors = get_prime_factors(n)
    divisors_ = []
    hq.heapify(divisors_)
    rec_permuts(0, prime_factors, 1, divisors_)
    print('excluding from heap...')
    return [hq.heappop(divisors_) for _ in range(len(divisors_))]


def get_prime_factors(n: int) -> d[int, int]:
    prime_factors = d(int)
    for prime in PRIMES:
        if prime ** 2 > n:
            break
        while n % prime == 0:
            n //= prime
            prime_factors[prime] += 1
    if n != 1:
        prime_factors[n] += 1
    print(f'{prime_factors = }')
    return prime_factors


def rec_permuts(prev_pf: int, prime_factors: d[int, int], divisor_: int, divisors_: list[int]):
    # adding divisor to divisors:
    hq.heappush(divisors_, divisor_)
    # body of rec:
    for prime_factor in prime_factors.keys():
        if prime_factor >= prev_pf and prime_factors[prime_factor]:
            prime_factors[prime_factor] -= 1
            rec_permuts(prime_factor, prime_factors, divisor_ * prime_factor, divisors_)
            prime_factors[prime_factor] += 1


n_ = 164171010688258216356020741663906501410127235530735881272116103087925094171390144280159034536439457734870419127140401667195510331085657185332721089236401193044493457116299768844344303479235489462436380672117015123283299131391904179287678259173308536738761981139958654880852234908448338817289014166774169869251339379828599748492918775437864739032217778051333882990074116246281269364933724892342134504702491040016637557429810893780765197418589477584716543480995722533317862352141459217781316266211186486157019262080414077670264642736018426998113523445732680856144329876972273300703392584997729207197971083945700345494092400147186997307012069454068489589035676979448169848060836924945824197706493306108258511936030341393221586423523264452449403781993352421885094664052270795527632721896121424813173522474674395886155092203404036730748474781710715745446135468098139831824083259647919175273503681561172684624283384438504776503000432241604550454374116320822227191911322123484085063926350606342197146407841178028071147192533942517270553513988142925976090769695456221159699052583533011331652079347093098173086975483539274464023357456484465482927479569437320368592222760278170306076733438801098370797675711274671054970711442158930561684343135774118741594506702833147396758825015850042983343690345185995956235143825771620543546030664562647854656431302644574119873820215595718618624485232422006575550007068883734241454686368856734496265385908809403972494685137741122866896719678053937285818409751670320140501843039224040735870096889596273419106389103662095318937990625980136711988237421962315266686856089505981438440850638067589321141759499017023839596858455548192000140085142294166987063499024792681334843159790936321351919859758669569200541507612099780909705198902176026219872201715422096090343686272984351441594569506778041062663266799342793856313801540959815845788584759033248828248561586450271172777240971795656082001848115815260930521663167480173886064019118572778281516735157779555888167787064432558595410843987446497881666288423233170060413025924629950477303342180149398926073618582715358742250388958231281694757980523791263699450732952325727664209947786063982561775327638504516918570101319391698412388607603742484414748268389669129118026878969735782286841116842656410574647607524418900720328045377993386279808768990376289424757351052369393977137871998119168898493037938756635621557623138404459266598837784229325799838782026060481496865561757031839002257091802876949248392744175669112242088439883248336310597001257385980776961529351198877747193531054956881808332177946751404038228718567911769630971553915410012677600002457982207465176670752102117002773980548089696530972476439694599881281812973217265853884727906535479745854085338851105144585481994156206497436745899944877732531412541279014300324594890623941145509856940982863769834430048120562966797907114102689879364945689860493474954538422367719507882513166051007352994068319251450666676648368200564329382998758875760414259654004977261309988267319806354856051784553990936610634733375984159028722378614984450255386315585631994503350002142910493190254825610707400589976364985748467955131077971641882672895854571236368282811336220769174784720113331269084746524204124263475054112841630933586166195036115696469686075600480420563557567616835633252622327172811002146392754445051182169805284630259703542633955126179520113059629914229833688535925729676778028406897316106101038469119090984567152591962365415039646394591503830797626339246986057077758611413664914168745375266786298141171496573941614387744125843685677063619782918759823106021054037757857761587472240835040580447360544029064930412569943169729238102162312218687930203068055400275795180972382856696655279408212344832
n__ = 7286909597654977561258926693618841354599667011087431101570452869551764619441044914577326267103601464828228739353536277078755918677550558558858385647924588864316056564327391934067709019202795268213458266761216787429001632832071720145142137677575011374143590872901036574197330639351647496532590659160272182372633896400127030062499619360919304673970075657107179931753765233204804477096811283
n___ = 1017415302352030715089769143357348066038940715680275093403532356967247053881971415924154307875126195181144966713795906009393501871305460253282512549667475865602197706338557828840807662550199994745943996831026024713187551905090158681972204476128171737889919463010962566053634193048517831502881062412069997630878688652427419979016823486265664182469880742969768189927177031592450053290125300894165590352733518865802041709096148680776407259818859162938058592329462337046795091684513027588020962336990933021796980150463077321718173384728593730858959098165580448488239190316889547522242076800717459167679296157119404073027879501664151558287385243372356705853569780850476484294556853070539355586674794822216241974835246454146885482944683158189778192833311376580370860261177427143781241376384453306053982418452518819201209266831537086242982500183977176574031455946171843254958503553554535661662587077026270023109732412047413672167431005140581854420066721003888857500354912764817728052800247517386680268533261424069820687977908761560004091859025027816814775122725405952588076189788163356304524918574527995660275652138417429073025305296447817989701401950927198633547208943525009667558675138398297787933604069892809947801293714879089659748140160372407056578724855597381689563499055653229440283525359383865895250571784727613836482929178417513382920487258547250419948337998608600959234983041347288670100738307533364685547156110360251428815049331731683019910000201915999971620308522378562075554004605450846503778554147119680891407513134139190133527859725019221333819011370679934879758132208302026512742391778088266647028886566753865942324486807020510184276210481223168
n_x = 1249119881833535095502046033930809210542076850555592608768

divs = divisors(n___)
print(f'res: {divs}')
print(f'size: {len(divs)}')