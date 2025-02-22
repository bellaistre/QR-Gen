import random
import requests
import re
import ast

import cProfile


L_GROUPS = [
    (0 << 24) | (0 << 16) | (0 << 8) | 0,
    (1 << 24) | (19 << 16) | (0 << 8) | 0,
    (1 << 24) | (34 << 16) | (0 << 8) | 0,
    (1 << 24) | (55 << 16) | (0 << 8) | 0,
    (1 << 24) | (80 << 16) | (0 << 8) | 0,
    (1 << 24) | (108 << 16) | (0 << 8) | 0,
    (2 << 24) | (68 << 16) | (0 << 8) | 0,
    (2 << 24) | (78 << 16) | (0 << 8) | 0,
    (2 << 24) | (97 << 16) | (0 << 8) | 0,
    (2 << 24) | (116 << 16) | (0 << 8) | 0,
    (2 << 24) | (68 << 16) | (2 << 8) | 69,
    (4 << 24) | (81 << 16) | (0 << 8) | 0,
    (2 << 24) | (92 << 16) | (2 << 8) | 93,
    (4 << 24) | (107 << 16) | (0 << 8) | 0,
    (3 << 24) | (115 << 16) | (1 << 8) | 116,
    (5 << 24) | (87 << 16) | (1 << 8) | 88,
    (5 << 24) | (98 << 16) | (1 << 8) | 99,
    (1 << 24) | (107 << 16) | (5 << 8) | 108,
    (5 << 24) | (120 << 16) | (1 << 8) | 121,
    (3 << 24) | (113 << 16) | (4 << 8) | 114,
    (3 << 24) | (107 << 16) | (5 << 8) | 108,
    (4 << 24) | (116 << 16) | (4 << 8) | 117,
    (2 << 24) | (111 << 16) | (7 << 8) | 112,
    (4 << 24) | (121 << 16) | (5 << 8) | 122,
    (6 << 24) | (117 << 16) | (4 << 8) | 118,
    (8 << 24) | (106 << 16) | (4 << 8) | 107,
    (10 << 24) | (114 << 16) | (2 << 8) | 115,
    (8 << 24) | (122 << 16) | (4 << 8) | 123,
    (3 << 24) | (117 << 16) | (10 << 8) | 118,
    (7 << 24) | (116 << 16) | (7 << 8) | 117,
    (5 << 24) | (115 << 16) | (10 << 8) | 116,
    (13 << 24) | (115 << 16) | (3 << 8) | 116,
    (17 << 24) | (115 << 16) | (0 << 8) | 0,
    (17 << 24) | (115 << 16) | (1 << 8) | 116,
    (13 << 24) | (115 << 16) | (6 << 8) | 116,
    (12 << 24) | (121 << 16) | (7 << 8) | 122,
    (6 << 24) | (121 << 16) | (14 << 8) | 122,
    (17 << 24) | (122 << 16) | (4 << 8) | 123,
    (4 << 24) | (122 << 16) | (18 << 8) | 123,
    (20 << 24) | (117 << 16) | (4 << 8) | 118,
    (19 << 24) | (118 << 16) | (6 << 8) | 119,
]

M_GROUPS = [
    (0 << 24) | (0 << 16) | (0 << 8) | 0,
    (1 << 24) | (16 << 16) | (0 << 8) | 0,
    (1 << 24) | (28 << 16) | (0 << 8) | 0,
    (1 << 24) | (44 << 16) | (0 << 8) | 0,
    (2 << 24) | (32 << 16) | (0 << 8) | 0,
    (2 << 24) | (43 << 16) | (0 << 8) | 0,
    (4 << 24) | (27 << 16) | (0 << 8) | 0,
    (4 << 24) | (31 << 16) | (0 << 8) | 0,
    (2 << 24) | (38 << 16) | (2 << 8) | 39,
    (3 << 24) | (36 << 16) | (2 << 8) | 37,
    (4 << 24) | (43 << 16) | (1 << 8) | 44,
    (1 << 24) | (50 << 16) | (4 << 8) | 51,
    (6 << 24) | (36 << 16) | (2 << 8) | 37,
    (8 << 24) | (37 << 16) | (1 << 8) | 38,
    (4 << 24) | (40 << 16) | (5 << 8) | 41,
    (5 << 24) | (41 << 16) | (5 << 8) | 42,
    (7 << 24) | (45 << 16) | (3 << 8) | 46,
    (10 << 24) | (46 << 16) | (1 << 8) | 47,
    (9 << 24) | (43 << 16) | (4 << 8) | 44,
    (3 << 24) | (44 << 16) | (11 << 8) | 45,
    (3 << 24) | (41 << 16) | (13 << 8) | 42,
    (17 << 24) | (42 << 16) | (0 << 8) | 0,
    (17 << 24) | (46 << 16) | (0 << 8) | 0,
    (4 << 24) | (47 << 16) | (14 << 8) | 48,
    (6 << 24) | (45 << 16) | (14 << 8) | 46,
    (8 << 24) | (47 << 16) | (13 << 8) | 48,
    (19 << 24) | (46 << 16) | (4 << 8) | 47,
    (22 << 24) | (45 << 16) | (3 << 8) | 46,
    (3 << 24) | (45 << 16) | (23 << 8) | 46,
    (21 << 24) | (45 << 16) | (7 << 8) | 46,
    (19 << 24) | (47 << 16) | (10 << 8) | 48,
    (2 << 24) | (46 << 16) | (29 << 8) | 47,
    (10 << 24) | (46 << 16) | (23 << 8) | 47,
    (14 << 24) | (46 << 16) | (21 << 8) | 47,
    (14 << 24) | (46 << 16) | (23 << 8) | 47,
    (12 << 24) | (47 << 16) | (26 << 8) | 48,
    (6 << 24) | (47 << 16) | (34 << 8) | 48,
    (29 << 24) | (46 << 16) | (14 << 8) | 47,
    (13 << 24) | (46 << 16) | (32 << 8) | 47,
    (40 << 24) | (47 << 16) | (7 << 8) | 48,
    (18 << 24) | (47 << 16) | (31 << 8) | 48,
]

Q_GROUPS = [
    (0 << 24) | (0 << 16) | (0 << 8) | 0,
    (1 << 24) | (13 << 16) | (0 << 8) | 0,
    (1 << 24) | (22 << 16) | (0 << 8) | 0,
    (2 << 24) | (17 << 16) | (0 << 8) | 0,
    (2 << 24) | (24 << 16) | (0 << 8) | 0,
    (2 << 24) | (15 << 16) | (2 << 8) | 16,
    (4 << 24) | (19 << 16) | (0 << 8) | 0,
    (2 << 24) | (14 << 16) | (4 << 8) | 15,
    (4 << 24) | (18 << 16) | (2 << 8) | 19,
    (4 << 24) | (16 << 16) | (4 << 8) | 17,
    (6 << 24) | (19 << 16) | (2 << 8) | 20,
    (4 << 24) | (22 << 16) | (4 << 8) | 23,
    (4 << 24) | (20 << 16) | (6 << 8) | 21,
    (8 << 24) | (20 << 16) | (4 << 8) | 21,
    (11 << 24) | (16 << 16) | (5 << 8) | 17,
    (5 << 24) | (24 << 16) | (7 << 8) | 25,
    (15 << 24) | (19 << 16) | (2 << 8) | 20,
    (1 << 24) | (22 << 16) | (15 << 8) | 23,
    (17 << 24) | (22 << 16) | (1 << 8) | 23,
    (17 << 24) | (21 << 16) | (4 << 8) | 22,
    (15 << 24) | (24 << 16) | (5 << 8) | 25,
    (17 << 24) | (22 << 16) | (6 << 8) | 23,
    (7 << 24) | (24 << 16) | (16 << 8) | 25,
    (11 << 24) | (24 << 16) | (14 << 8) | 25,
    (11 << 24) | (24 << 16) | (16 << 8) | 25,
    (7 << 24) | (24 << 16) | (22 << 8) | 25,
    (28 << 24) | (22 << 16) | (6 << 8) | 23,
    (8 << 24) | (23 << 16) | (26 << 8) | 24,
    (4 << 24) | (24 << 16) | (31 << 8) | 25,
    (1 << 24) | (23 << 16) | (37 << 8) | 24,
    (15 << 24) | (24 << 16) | (25 << 8) | 25,
    (42 << 24) | (24 << 16) | (1 << 8) | 25,
    (10 << 24) | (24 << 16) | (35 << 8) | 25,
    (29 << 24) | (24 << 16) | (19 << 8) | 25,
    (44 << 24) | (24 << 16) | (7 << 8) | 25,
    (39 << 24) | (24 << 16) | (14 << 8) | 25,
    (46 << 24) | (24 << 16) | (10 << 8) | 25,
    (49 << 24) | (24 << 16) | (10 << 8) | 25,
    (48 << 24) | (24 << 16) | (14 << 8) | 25,
    (43 << 24) | (24 << 16) | (22 << 8) | 25,
    (34 << 24) | (24 << 16) | (34 << 8) | 25,
]

H_GROUPS = [
    (0 << 24) | (0 << 16) | (0 << 8) | 0,
    (1 << 24) | (9 << 16) | (0 << 8) | 0,
    (1 << 24) | (16 << 16) | (0 << 8) | 0,
    (2 << 24) | (13 << 16) | (0 << 8) | 0,
    (4 << 24) | (9 << 16) | (0 << 8) | 0,
    (2 << 24) | (11 << 16) | (2 << 8) | 12,
    (4 << 24) | (15 << 16) | (0 << 8) | 0,
    (4 << 24) | (13 << 16) | (1 << 8) | 14,
    (4 << 24) | (14 << 16) | (2 << 8) | 15,
    (4 << 24) | (12 << 16) | (4 << 8) | 13,
    (6 << 24) | (15 << 16) | (2 << 8) | 16,
    (3 << 24) | (12 << 16) | (8 << 8) | 13,
    (7 << 24) | (14 << 16) | (4 << 8) | 15,
    (12 << 24) | (11 << 16) | (4 << 8) | 12,
    (11 << 24) | (12 << 16) | (5 << 8) | 13,
    (11 << 24) | (12 << 16) | (7 << 8) | 13,
    (3 << 24) | (15 << 16) | (13 << 8) | 16,
    (2 << 24) | (14 << 16) | (17 << 8) | 15,
    (2 << 24) | (14 << 16) | (19 << 8) | 15,
    (9 << 24) | (13 << 16) | (16 << 8) | 14,
    (15 << 24) | (15 << 16) | (10 << 8) | 16,
    (19 << 24) | (16 << 16) | (6 << 8) | 17,
    (34 << 24) | (13 << 16) | (0 << 8) | 0,
    (16 << 24) | (15 << 16) | (14 << 8) | 16,
    (30 << 24) | (16 << 16) | (2 << 8) | 17,
    (22 << 24) | (15 << 16) | (13 << 8) | 16,
    (33 << 24) | (16 << 16) | (4 << 8) | 17,
    (12 << 24) | (15 << 16) | (28 << 8) | 16,
    (11 << 24) | (15 << 16) | (31 << 8) | 16,
    (19 << 24) | (15 << 16) | (26 << 8) | 16,
    (23 << 24) | (15 << 16) | (25 << 8) | 16,
    (23 << 24) | (15 << 16) | (28 << 8) | 16,
    (19 << 24) | (15 << 16) | (35 << 8) | 16,
    (11 << 24) | (15 << 16) | (46 << 8) | 16,
    (59 << 24) | (16 << 16) | (1 << 8) | 17,
    (22 << 24) | (15 << 16) | (41 << 8) | 16,
    (2 << 24) | (15 << 16) | (64 << 8) | 16,
    (24 << 24) | (15 << 16) | (46 << 8) | 16,
    (42 << 24) | (15 << 16) | (32 << 8) | 16,
    (10 << 24) | (15 << 16) | (67 << 8) | 16,
    (20 << 24) | (15 << 16) | (61 << 8) | 16,
]


def ecc_to_groups(quality, version):
    if quality == 0:
        groups_bits = L_GROUPS[version]
    if quality == 1:
        groups_bits = M_GROUPS[version]
    if quality == 2:
        groups_bits = Q_GROUPS[version]
    if quality == 3:
        groups_bits = H_GROUPS[version]

    grp1 = (groups_bits >> 24) & 0xFF
    grp2 = (groups_bits >> 16) & 0xFF
    grp3 = (groups_bits >> 8) & 0xFF
    grp4 = (groups_bits >> 0) & 0xFF

    return [
        (grp1, grp2),
        (grp3, grp4),
    ]


q_to_ect = {
    0: "L",
    1: "M",
    2: "Q",
    3: "H"
}


L_ECT = [
    0, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30,
    30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
]

M_ECT = [
    0, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28,
    28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28,
]

Q_ECT = [
    0, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30,
    30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
]

H_ECT = [
    0, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30,
    30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
]


def ecc_to_ect(quality, version):
    if quality == 0:
        return L_ECT[version]
    if quality == 1:
        return M_ECT[version]
    if quality == 2:
        return Q_ECT[version]
    if quality == 3:
        return H_ECT[version]


headers = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


pattern = re.compile(
    r'<p>The division has been performed [^<]*</p><p>([^<]*)<')
pattern_error = re.compile(
    r'''Use the result from step 1b to perform the next XOR.
</p>
<p>\(0'''
)

session = requests.Session()


def get_error_codes(coeffs, version):
    msg_coeff = '%2C'.join([str(e) for e in coeffs])

    url = f"https://www.thonky.com/qr-code-tutorial/show-division-steps?msg_coeff={msg_coeff}&num_ecc_blocks={version}"
    r = session.get(url, headers=headers)

    text = r.text

    if pattern_error.search(text):
        raise Exception("Invalid test")

    for match in re.finditer(pattern, text):
        whole_content = match.group(1)
        needed = whole_content.replace("&nbsp; ", ",")

    res = ast.literal_eval(f'[{needed}]')
    if len(res) != version:
        res = ([0] * (version - len(res))) + res
    return res


def structure(seed=1):
    random.seed(seed)

    version = random.randint(1, 40)
    quality = random.randint(0, 3)

    [(grp1_size, grp1_count), (grp2_size, grp2_count)
     ] = ecc_to_groups(quality, version)

    print("//", {"seed": seed, "version": version, "quality": quality})

    data_codes = ([[random.randint(0, 254) for _ in range(
        grp1_count)] for _ in range(grp1_size)] +
        [[random.randint(0, 254) for _ in range(
            grp2_count)] for _ in range(grp2_size)])

    print("// Download error: START")
    error_code_size = ecc_to_ect(quality, version)
    error_codes = [
        get_error_codes(e, error_code_size) for e in data_codes
    ]

    print("// Download error: DONE")

    res_data = []
    for j in range(grp1_count):
        for i in range(grp1_size + grp2_size):
            res_data.append(data_codes[i][j])

    for j in range(grp1_count, grp2_count):
        for i in range(grp1_size, grp1_size + grp2_size):
            res_data.append(data_codes[i][j])

    res_error = []
    for j in range(error_code_size):
        for i in range(grp1_size + grp2_size):
            res_error.append(error_codes[i][j])

    flat_data = [item for sublist in data_codes for item in sublist]
    # flat_error = [item for sublist in error_codes for item in sublist]

    return (f"""
#[test]
fn structure_codewords_seed_{seed}() {{
    const VERSION: usize = {version};
    const QUALITY: crate::vecl::ECL = crate::vecl::ECL::{q_to_ect[quality]};

    let data_codewords = &{flat_data}
    .to_vec();
    let error_codewords =
        crate::polynomials::GENERATOR_POLYNOMIALS[crate::vecl::ecc_to_ect(QUALITY, VERSION)];

    let structure =
        crate::polynomials::structure(&data_codewords, &error_codewords, QUALITY, VERSION);

    assert_eq!(
        structure[..data_codewords.len()].len(),
        {len(res_data)}
    );
    assert_eq!(
        structure[..data_codewords.len()],
        {res_data}
        .to_vec()
    );

    assert_eq!(
        structure[data_codewords.len()..].len(),
        {len(res_error)}
    );
    assert_eq!(
        structure[data_codewords.len()..],
        {res_error}
        .to_vec()
    );
}}
""")


results = []
for i in range(100, 150):
    try:
        res = structure(i)
        if res:
            results.append(res)
    except:
        pass

for r in results:
    print(r)
