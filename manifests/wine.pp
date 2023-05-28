# wine
class ytlaces::wine(
  String $username = 'tsutsumi'
) {
  package {'wine':}
  package {'wine-gecko':}
}
