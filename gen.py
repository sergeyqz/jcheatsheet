import csv
import html

from markdown import markdown


row_template = """
<tr class="{type}">
    <td class="name"><a class="link" href="https://code.jsoftware.com/wiki/Vocabulary/{link}">{name}</a></td>
    <td class="code">{indent}{left_rank}{code} <span class="rank">{right_rank}</span> </td>
    <td class="desc">{desc}</td>
</tr>
"""

with open('data.tsv') as f:
    [f.readline() for _ in range(2)]  # Drop Done, Total lines
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    rows = list(reader)[:-1]  # Drop the lhs_max_length line

# lhs_max_length = int(rows[-1]['lhsLength'])
lhs_max_length = 0

for r in rows:
    r['lhs'] = ''.join([
        f'[{r["LN"]}]' if r['Opt'] else r['LN'], ' ' if r['LN'] else '',
        r['LMO'],                                ' ' if r['LMO'] else ''])
    l = (len(r['LR'])+1) if r['LR'] else 0
    r['lhsLength'] = l+len(r['lhs'])
    lhs_max_length = max(lhs_max_length, r['lhsLength'])

rendered_rows = []
for r in rows:
    for k in ('', 'full'): del r[k]
    desc = r['Description']
    for k in ('RN', 'LN', 'RMO', 'LMO'):
        desc = desc.replace(k, r[k])
    indent = lhs_max_length - int(r['lhsLength'])
    code = [
        f'[{r["LN"]}]' if r['Opt'] else r['LN'],
        ' ' if r['LN'] else '',
        r['LMO'],
        ' ' if r['LMO'] else '',
        r['P'],
        ' ' if r['RMO'] else '',
        r['RMO'],
        ' ' if r['RN'] else '',
        r['RN'],
    ]
    d = {
        'link': r['Link'],
        'type': r['Type'],
        'name': r['Name'],
        'desc': markdown(desc)[3:-4],
        'indent': '&nbsp;'*indent,
        'code': html.escape(''.join(code)),
        'left_rank': f'<span class="rank">{r["LR"]}</span>&nbsp;' if r['LR'] else '',
        'right_rank': r['RR'],
    }
    rendered_rows.append(row_template.format(**d))

with open('index-template.html') as f:
    template = f.read()
with open('index.html', 'w') as f:
    f.write(template.replace('INSERT-ROWS', ''.join(rendered_rows)))
