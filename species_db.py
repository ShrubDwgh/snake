"""
Knowledge base spesies ular.
Setiap spesies punya: nama umum, nama ilmiah, deskripsi,
tingkat risiko, saran tindakan, habitat, dan distribusi.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    HIGH   = "TINGGI"
    MEDIUM = "SEDANG"
    LOW    = "RENDAH"


@dataclass
class SpeciesInfo:
    common_name: str
    scientific_name: str
    description: str
    is_venomous: bool
    risk_level: RiskLevel
    actions: List[str]
    habitat: str
    distribution: str
    fun_fact: Optional[str] = None


SNAKE_DB: dict[str, SpeciesInfo] = {

    # ══════════════════════════════════════════
    #  BERBISA — RISIKO TINGGI
    # ══════════════════════════════════════════

    "king_cobra": SpeciesInfo(
        common_name    = "King Cobra",
        scientific_name= "Ophiophagus hannah",
        description    = (
            "Ular berbisa terpanjang di dunia, bisa mencapai 5.5 meter. "
            "Bisanya bersifat neurotoksik (merusak sistem saraf) dengan dosis "
            "yang dapat membunuh gajah muda. Mampu 'berdiri' hingga sepertiga "
            "tubuhnya dan mengeluarkan suara mendesis keras saat terancam."
        ),
        is_venomous    = True,
        risk_level     = RiskLevel.HIGH,
        actions        = [
            "🚨 DARURAT — Hubungi 119 atau pergi ke IGD segera",
            "Jauhi ular, jangan mencoba menangkap atau membunuh",
            "Imobilisasi anggota tubuh yang terkena, jaga tetap di bawah jantung",
            "Lepas cincin, jam, atau pakaian ketat di sekitar luka",
            "JANGAN isap luka, toreh, atau pasang tourniquet",
            "Catat waktu gigitan dan foto ular dari jarak aman jika bisa",
            "Minta antivenom (SABU) di rumah sakit — tersedia di RS besar",
        ],
        habitat        = "Hutan hujan tropis, tepi sungai, ladang, area dengan banyak ular lain (mangsa utamanya)",
        distribution   = "Sumatera, Jawa, Kalimantan, Sulawesi, dan pulau-pulau sekitarnya",
        fun_fact       = "King Cobra adalah satu-satunya ular yang membangun sarang untuk telurnya.",
    ),

    "chain_viper": SpeciesInfo(
        common_name    = "Ular Tanah / Russell's Viper",
        scientific_name= "Daboia russelii",
        description    = (
            "Salah satu ular paling mematikan di Asia. Bisanya hemotoksik — "
            "merusak sel darah merah dan mengganggu pembekuan darah, menyebabkan "
            "pendarahan internal. Pola tubuh seperti rantai cokelat di atas latar "
            "kuning-abu membuatnya mudah dikenali."
        ),
        is_venomous    = True,
        risk_level     = RiskLevel.HIGH,
        actions        = [
            "🚨 DARURAT — Ini gawat darurat medis, segera ke IGD",
            "Berbaring dan batasi semua gerakan tubuh",
            "Imobilisasi anggota tubuh dengan bidai darurat (kayu, karton)",
            "Lepas semua perhiasan — area gigitan bisa bengkak cepat",
            "JANGAN konsumsi alkohol, aspirin, atau obat pengencer darah",
            "Antivenom Russell's Viper tersedia di RS rujukan",
        ],
        habitat        = "Savana, padang rumput kering, tepi hutan, ladang pertanian",
        distribution   = "Asia Selatan, sebagian Asia Tenggara termasuk Indonesia bagian barat",
    ),

    "banded_krait": SpeciesInfo(
        common_name    = "Ular Welang",
        scientific_name= "Bungarus fasciatus",
        description    = (
            "Ular berbisa dengan pola belang hitam-kuning mencolok. Aktif malam hari, "
            "relatif jinak di siang hari. BERBAHAYA karena gigitannya sering tidak "
            "terasa sakit sehingga korban terlambat ke RS. Bisanya neurotoksik kuat, "
            "menyerang sistem saraf pusat."
        ),
        is_venomous    = True,
        risk_level     = RiskLevel.HIGH,
        actions        = [
            "🚨 Pergi ke IGD SEGERA meski gigitan tidak terasa sakit",
            "Gejala (sesak napas, kelumpuhan) bisa muncul 1-6 jam kemudian",
            "Berbaring diam, jangan panik dan batasi gerak",
            "Hubungi BPBD (021-122) jika di daerah terpencil",
            "JANGAN tunggu gejala muncul — segera ke RS",
        ],
        habitat        = "Hutan, ladang, pinggir sungai, area sekitar air",
        distribution   = "Sumatera, Jawa, Kalimantan, Sulawesi",
        fun_fact       = "Welang sering disalahartikan sebagai tidak berbahaya karena ukurannya yang tidak terlalu besar.",
    ),

    "malayan_pit_viper": SpeciesInfo(
        common_name    = "Ular Gibug / Malayan Pit Viper",
        scientific_name= "Calloselasma rhodostoma",
        description    = (
            "Penyebab utama kasus gigitan ular di Asia Tenggara. Pola tubuhnya "
            "menyerupai daun kering di tanah — sangat sulit terlihat. Bisanya "
            "hemotoksik dan dapat menyebabkan nekrosis (kematian jaringan) parah "
            "di sekitar luka gigitan."
        ),
        is_venomous    = True,
        risk_level     = RiskLevel.HIGH,
        actions        = [
            "🚨 Segera ke IGD — nekrosis jaringan bisa terjadi dalam jam pertama",
            "Cuci luka perlahan dengan air bersih dan sabun",
            "Imobilisasi anggota tubuh — jangan gerakkan",
            "JANGAN gunakan tourniquet atau es batu",
            "Antivenom tersedia di RS besar di Sumatera dan Jawa",
        ],
        habitat        = "Perkebunan karet dan kopi, hutan sekunder, tepi jalan",
        distribution   = "Sumatera, Jawa, Kalimantan bagian barat",
    ),

    "monocled_cobra": SpeciesInfo(
        common_name    = "Kobra Monokol / Ular Sendok",
        scientific_name= "Naja kaouthia",
        description    = (
            "Kobra dengan tanda bulat seperti kacamata (monokol) di bagian belakang "
            "tudungnya. Bisanya neurotoksik dan sitotoksik. Mampu meludahkan bisa "
            "tepat ke mata hingga jarak 2-3 meter, menyebabkan kebutaan sementara "
            "atau permanen jika tidak segera ditangani."
        ),
        is_venomous    = True,
        risk_level     = RiskLevel.HIGH,
        actions        = [
            "Jika bisa kena MATA: cuci dengan air mengalir 15-20 menit, segera ke dokter",
            "Jika digigit: segera ke IGD",
            "Buka tudung cobra = tanda menyerang, mundur perlahan jangan lari",
            "Antivenom cobra tersedia di RS rujukan",
        ],
        habitat        = "Sawah, ladang, tepi hutan, pemukiman pedesaan",
        distribution   = "Sumatera, Jawa, Kalimantan",
    ),

    # ══════════════════════════════════════════
    #  BERBISA — RISIKO SEDANG
    # ══════════════════════════════════════════

    "green_pit_viper": SpeciesInfo(
        common_name    = "Ular Bangkai Laut Hijau",
        scientific_name= "Trimeresurus albolabris",
        description    = (
            "Ular pohon berwarna hijau cerah dengan mata merah atau kuning. "
            "Bisanya hemotoksik namun jarang fatal pada orang dewasa sehat. "
            "Sangat kamuflase di dedaunan dan sering mengejutkan orang yang "
            "tidak sengaja menyentuh ranting tempatnya bertengger."
        ),
        is_venomous    = True,
        risk_level     = RiskLevel.MEDIUM,
        actions        = [
            "Segera ke puskesmas atau rumah sakit terdekat",
            "Pantau pembengkakan — bisa meluas dalam 2-3 jam",
            "Lepas perhiasan dan pakaian ketat di sekitar luka",
            "Tetap tenang dan batasi gerakan",
        ],
        habitat        = "Pohon dan semak di hutan, taman kota, kebun",
        distribution   = "Seluruh Indonesia, sangat umum di Jawa dan Bali",
        fun_fact       = "Jantan dan betina bisa berbeda warna — jantan hijau, betina kadang kemerahan.",
    ),

    # ══════════════════════════════════════════
    #  TIDAK BERBISA
    # ══════════════════════════════════════════

    "reticulated_python": SpeciesInfo(
        common_name    = "Sanca Kembang",
        scientific_name= "Malayopython reticulatus",
        description    = (
            "Ular terpanjang di dunia — rekor resmi 7.67 meter. Tidak berbisa "
            "tapi berbahaya karena kekuatan lilitannya luar biasa. Pola tubuh "
            "menyerupai jaring geometris dengan warna cokelat, hitam, dan kuning. "
            "Umumnya tidak menyerang manusia kecuali terprovokasi."
        ),
        is_venomous    = False,
        risk_level     = RiskLevel.MEDIUM,
        actions        = [
            "Jangan dekati atau provokasi — bisa melilit kuat",
            "Hubungi BPBD (021-122) atau BKSDA untuk evakuasi profesional",
            "Jika tergigit: cuci luka sabun dan air, cek tetanus",
            "Jika terlilit: jangan panik, minta bantuan orang lain segera",
        ],
        habitat        = "Hutan hujan, tepi sungai, kebun, kadang masuk pemukiman",
        distribution   = "Seluruh Indonesia — salah satu reptil paling tersebar luas",
        fun_fact       = "Sanca kembang bisa bertahan 1-2 tahun tanpa makan setelah menelan mangsa besar.",
    ),

    "rat_snake": SpeciesInfo(
        common_name    = "Ular Tikus / Ular Jali",
        scientific_name= "Ptyas mucosa",
        description    = (
            "Ular besar tidak berbisa, sahabat petani karena memangsa tikus. "
            "Sering disalahartikan sebagai kobra karena bisa mendirikan tubuh bagian "
            "depan dan mengeluarkan suara mendesis keras. Warna tubuh abu-abu kehijauan "
            "dengan corak seperti jaring di bagian belakang."
        ),
        is_venomous    = False,
        risk_level     = RiskLevel.LOW,
        actions        = [
            "Tidak perlu panik — ular ini tidak berbahaya",
            "Biarkan pergi dengan sendirinya atau hubungi komunitas reptil",
            "Jika tergigit: cuci dengan sabun dan air, tidak perlu antivenom",
            "Mohon jangan dibunuh — berperan penting kendalikan hama tikus",
        ],
        habitat        = "Sawah, kebun, gudang padi, pemukiman pedesaan",
        distribution   = "Seluruh Indonesia, sangat umum",
        fun_fact       = "Ular tikus bisa berlari sangat cepat — hingga 10 km/jam di permukaan tanah.",
    ),

    "golden_tree_snake": SpeciesInfo(
        common_name    = "Ular Terbang / Golden Tree Snake",
        scientific_name= "Chrysopelea ornata",
        description    = (
            "Ular ramping berwarna hijau-hitam yang bisa meluncur dari pohon ke pohon "
            "dengan meratakan tubuhnya menjadi bentuk 'C'. Punya bisa ringan yang hanya "
            "efektif pada kadal kecil dan katak. Praktis tidak berbahaya bagi manusia."
        ),
        is_venomous    = False,
        risk_level     = RiskLevel.LOW,
        actions        = [
            "Tidak berbahaya bagi manusia, santai saja",
            "Cuci luka jika tidak sengaja tergigit",
            "Biarkan pergi — dia juga tidak mau berinteraksi dengan kamu",
        ],
        habitat        = "Tajuk pohon, taman kota, hutan sekunder",
        distribution   = "Jawa, Bali, Sumatera, Kalimantan",
        fun_fact       = "Satu-satunya ular di Indonesia yang bisa 'terbang' — meluncur hingga 10 meter antar pohon.",
    ),

    "green_vine_snake": SpeciesInfo(
        common_name    = "Ular Cambuk Hijau",
        scientific_name= "Ahaetulla nasuta",
        description    = (
            "Ular paling ramping di Indonesia — sebesar pensil tapi bisa sepanjang 2 meter. "
            "Warna hijau terang membuatnya nyaris tidak terlihat di antara dedaunan. "
            "Bisa sangat lemah, hanya efektif melumpuhkan kadal dan katak kecil."
        ),
        is_venomous    = False,
        risk_level     = RiskLevel.LOW,
        actions        = [
            "Tidak berbahaya bagi manusia",
            "Bersihkan luka jika tergigit",
            "Ke dokter hanya jika ada reaksi alergi tidak biasa",
        ],
        habitat        = "Semak belukar, tepi hutan, kebun",
        distribution   = "Asia Tenggara, tersebar di seluruh Indonesia",
        fun_fact       = "Ular cambuk punya mata seperti kunci lobang — memberikan penglihatan binokular yang tajam.",
    ),
}


def get_species(class_name: str) -> SpeciesInfo | None:
    return SNAKE_DB.get(class_name)

def all_classes() -> list[str]:
    return list(SNAKE_DB.keys())
