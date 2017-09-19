# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generate mathops.py, the lookup tables giving information about dalvik math operations by opcode
if __name__ == "__main__":
    unary = 'ineg inot lneg lnot fneg dneg i2l i2f i2d l2i l2f l2d f2i f2l f2d d2i d2l d2f i2b i2c i2s'
    binary = 'iadd isub imul idiv irem iand ior ixor ishl ishr iushr ladd lsub lmul ldiv lrem land lor lxor lshl lshr lushr fadd fsub fmul fdiv frem dadd dsub dmul ddiv drem'
    binary = binary + ' ' + binary
    binlit = 'iadd isub imul idiv irem iand ior ixor '
    binlit = binlit + binlit + 'ishl ishr iushr'
    stypes = dict(zip('ifldbcs', 'INT FLOAT LONG DOUBLE INT INT INT'.split()))

    print('''
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Autogenerated by genmathops.py - do not edit''')
    print('from . import jvmops')
    print('from . import scalartypes as scalars')

    print('UNARY = {')
    for i, code in enumerate(unary.split()):
        code = code.replace('not','xor')
        if '2' in code:
            srct = stypes[code[0]]
            destt = stypes[code[2]]
        else:
            srct = destt = stypes[code[0]]
        print('    0x{:02X}: (jvmops.{}, scalars.{}, scalars.{}),'.format(i + 0x7b, code.upper(), srct, destt))
    print('}')

    print('BINARY = {')
    for i, code in enumerate(binary.split()):
        st = stypes[code[0]]
        # shift instructions have second arg an int even when operating on longs
        st2 = 'INT' if 'sh' in code else st
        print('    0x{:02X}: (jvmops.{}, scalars.{}, scalars.{}),'.format(i + 0x90, code.upper(), st, st2))
    print('}')

    print('BINARY_LIT = {')
    for i, code in enumerate(binlit.split()):
        print('    0x{:02X}: jvmops.{},'.format(i + 0xd0, code.upper()))
    print('}')