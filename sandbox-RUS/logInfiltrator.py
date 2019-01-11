def AttributeDict(self):
    return self

def HexBytes(self):
    return self

def r(mlog, fields):
    copy = dict(mlog)
    for k in fields:
        del copy[fields[k]]
    return copy


log = eval(input())

flds = ['chainId', 'condition', 'creates', 'gas', 'gasPrice', 'publicKey', 'r', 'raw', 's', 'standardV']

print(r(log, flds))
