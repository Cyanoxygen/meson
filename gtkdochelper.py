#!/usr/bin/env python3
# Copyright 2015 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, os
import subprocess
import shutil

def build_gtkdoc(source_root, build_root, doc_subdir, src_subdir, module):
    abs_src = os.path.join(source_root, src_subdir)
    abs_out = os.path.join(build_root, doc_subdir)
    htmldir = os.path.join(abs_out, 'html')
    subprocess.check_call(['gtkdoc-scan',
                           '--module=' + module,
                           '--source-dir=' + abs_src,
                           '--output-dir=.'], cwd=abs_out)
    subprocess.check_call(['gtkdoc-mkdb',
                           '--module=' + module,
                           '--output-format=xml',
                           '--source-dir=' + abs_src], cwd=abs_out)
    shutil.rmtree(htmldir, ignore_errors=True)
    try:
        os.mkdir(htmldir)
    except Exception:
        pass
    subprocess.check_call(['gtkdoc-mkhtml',
                           module,
                           '../%s-docs.xml' % module], cwd=htmldir)
    subprocess.check_call(['gtkdoc-fixxref',
                           '--module=' + module,
                           '--module-dir=html'], cwd=abs_out)

def install_gtkdoc(build_root, doc_subdir, install_prefix, datadir, module):
    source = os.path.join(build_root, doc_subdir, 'html')
    final_destination = os.path.join(install_prefix, datadir, module)
    shutil.rmtree(final_destination, ignore_errors=True)
    shutil.copytree(source, final_destination)

if __name__ == '__main__':
#    source_root = '/home/jpakkane/workspace/meson/test cases/frameworks/10 gtk-doc'
#    build_root = '/home/jpakkane/workspace/meson/work area'
#    doc_subdir = 'doc'
#    src_subdir = 'include'
#    module = 'foobar'
    if len(sys.argv) != 6:
        print(sys.argv)
        print("Bad arguments.")
        sys.exit(1)
    (source_root, build_root, doc_subdir, src_subdir, module) = sys.argv[1:]
    build_gtkdoc(source_root, build_root, doc_subdir, src_subdir, module)

    if 'MESON_INSTALL_PREFIX' in os.environ:
        if 'DESTDIR' in os.environ:
            installdir = os.environ['DESTDIR'] + os.environ['MESON_INSTALL_PREFIX']
        else:
            installdir = os.environ['MESON_INSTALL_PREFIX']
        install_gtkdoc(build_root, doc_subdir, installdir, 'share/gtk-doc/html', module)
