pkgname=menual
pkgver=0.0.1
pkgrel=1
pkgdesc="Menual is a fast desktop application launcher built with Python and Textual."
arch=('any')
url="https://github.com/FrancoisBasset/menual"
license=('MIT')
depends=('kitty' 'python>=3.14' 'python-textual')
makedepends=('python-build' 'python-installer' 'python-hatchling')

build() {
  cd "$startdir"
  /usr/bin/python -m build --wheel --no-isolation
}

package() {
  cd "$startdir"
  /usr/bin/python -m installer --destdir="$pkgdir" dist/*.whl
}
