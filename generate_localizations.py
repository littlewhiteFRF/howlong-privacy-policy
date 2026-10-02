#!/usr/bin/env python3
"""Generate the additional static locale sections for the HowLong web pages."""

from html import escape
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
EMAIL = "rolf1120802408@gmail.com"
POLICY_LINK = ROOT / "index.html"
SUPPORT_LINK = ROOT / "support" / "index.html"
URL_PATTERN = re.compile(r"https://[^\s<>\"']+")
TRAILING_PUNCTUATION = ".,;:!?，。；：！？、)]}”’"

TRANSLATION_NOTES = {
    "zh-Hant": "本頁為機器輔助翻譯，尚待母語人士審校。如發現內容不一致，請透過支援頁面聯絡我們。",
    "de": "Diese Übersetzung wurde maschinell erstellt und muss noch von Muttersprachlern geprüft werden. Wenn Ihnen eine Abweichung auffällt, kontaktieren Sie uns bitte über die Support-Seite.",
    "fr": "Cette traduction a été réalisée avec l’aide d’un outil automatique et doit encore être vérifiée par des locuteurs natifs. En cas de différence, contactez-nous depuis la page d’assistance.",
    "es-ES": "Esta traducción se ha generado con ayuda automática y aún debe ser revisada por hablantes nativos. Si detectas alguna diferencia, contáctanos desde la página de asistencia.",
    "pt-BR": "Esta tradução foi gerada com auxílio automático e ainda precisa de revisão por falantes nativos. Se encontrar alguma divergência, entre em contato pela página de suporte.",
    "ru": "Этот перевод подготовлен автоматически и еще требует проверки носителями языка. Если вы заметили расхождение, свяжитесь с нами через страницу поддержки.",
    "ar": "أُعدّت هذه الترجمة بمساعدة آلية وما زالت بحاجة إلى مراجعة متحدثين أصليين. إذا لاحظت اختلافًا، فتواصل معنا عبر صفحة الدعم.",
    "hi": "यह अनुवाद मशीन की सहायता से तैयार किया गया है और इसकी समीक्षा अभी मूल भाषा के वक्ताओं से होनी है। कोई अंतर दिखे तो सहायता पृष्ठ से हमसे संपर्क करें।",
    "mr": "हे भाषांतर मशीनच्या मदतीने तयार केले आहे आणि मूळ भाषिकांकडून त्याचे पुनरावलोकन होणे बाकी आहे. काही फरक आढळल्यास सहाय्य पृष्ठावरून आमच्याशी संपर्क साधा.",
    "bn": "এই অনুবাদটি যন্ত্রের সহায়তায় তৈরি করা হয়েছে এবং স্থানীয় ভাষাভাষীদের পর্যালোচনা এখনও বাকি। কোনো অমিল দেখলে সহায়তা পৃষ্ঠা থেকে যোগাযোগ করুন।",
    "id": "Terjemahan ini dibuat dengan bantuan mesin dan masih perlu ditinjau oleh penutur asli. Jika menemukan perbedaan, hubungi kami melalui halaman dukungan.",
    "vi": "Bản dịch này được tạo với sự hỗ trợ của máy và vẫn cần người bản ngữ xem lại. Nếu phát hiện điểm khác biệt, hãy liên hệ qua trang hỗ trợ.",
    "ja": "この翻訳は機械翻訳を利用しており、ネイティブによる確認が必要です。内容に相違がある場合は、サポートページからご連絡ください。",
    "ko": "이 번역은 기계 번역의 도움을 받아 작성되었으며 원어민 검토가 필요합니다. 내용에 차이가 있으면 지원 페이지를 통해 문의해 주세요.",
    "tr": "Bu çeviri makine yardımıyla hazırlanmıştır ve ana dili Türkçe olan kişilerce incelenmesi gerekir. Bir farklılık fark ederseniz destek sayfasından bize ulaşın.",
    "te": "ఈ అనువాదం యంత్ర సహాయంతో రూపొందించబడింది; మాతృభాష మాట్లాడేవారి సమీక్ష ఇంకా అవసరం. ఏదైనా తేడా కనిపిస్తే మద్దతు పేజీ ద్వారా మమ్మల్ని సంప్రదించండి.",
    "ur": "یہ ترجمہ مشینی مدد سے تیار کیا گیا ہے اور اسے مادری زبان بولنے والوں کی جانچ درکار ہے۔ کوئی فرق نظر آئے تو معاونت کے صفحے سے رابطہ کریں۔",
}


def attr(value: str) -> str:
    return escape(value, quote=True)


def linked_text(value: str) -> str:
    parts = []
    cursor = 0
    for match in URL_PATTERN.finditer(value):
        url = match.group(0)
        trimmed = url.rstrip(TRAILING_PUNCTUATION)
        parts.append(escape(value[cursor : match.start()]))
        parts.append(f'<a href="{attr(trimmed)}" rel="noreferrer">{escape(trimmed)}</a>')
        parts.append(escape(url[len(trimmed) :]))
        cursor = match.end()
    parts.append(escape(value[cursor:]))
    return "".join(parts)


def locale_id(locale: str) -> str:
    return locale.replace("-", "-")


def render_policy(entry: dict) -> str:
    locale = entry["locale"]
    locale_key = locale_id(locale)
    policy = entry["policy"]
    title_id = f"policy-title-{locale_key}"
    lines = [
        f'<section class="policy-card locale-section" id="privacy-{locale_key}" lang="{attr(locale)}" dir="{attr(entry["dir"])}" data-locale-section="{attr(locale)}" data-page-title="{attr(policy["title"])}" data-summary="{attr(policy["summary"])}" data-updated="{attr(policy["updated"])}" aria-labelledby="{title_id}">',
        '  <header class="policy-header">',
        '    <div>',
        f'      <p class="eyebrow">POLICY · {escape(locale.upper())}</p>',
        f'      <h2 class="policy-title" id="{title_id}">{escape(entry["name"])}</h2>',
        '    </div>',
        '    <p class="policy-header-note">HowLong</p>',
        '  </header>',
        '  <div class="policy-copy">',
    ]

    for section_index, section in enumerate(policy["sections"]):
        lines.append(f"    <h3>{escape(section['heading'])}</h3>")
        for paragraph in section.get("paragraphs", []):
            lines.append(f"    <p>{linked_text(paragraph)}</p>")
        if "items" in section:
            lines.append("    <ul>")
            lines.extend(f"      <li>{linked_text(item)}</li>" for item in section["items"])
            lines.append("    </ul>")
        if section_index == len(policy["sections"]) - 1:
            lines.append(f'    <p><a class="contact-link" href="mailto:{EMAIL}">{EMAIL}</a></p>')

    lines.extend(
        [
            f'    <p class="translation-note">{escape(TRANSLATION_NOTES[locale])}</p>',
            "  </div>",
            "</section>",
        ]
    )
    return "\n".join(lines)


def render_support(entry: dict) -> str:
    locale = entry["locale"]
    locale_key = locale_id(locale)
    support = entry["support"]
    lines = [
        f'<section class="localized-support" id="support-{locale_key}" lang="{attr(locale)}" dir="{attr(entry["dir"])}" data-locale-section="{attr(locale)}" data-page-title="{attr(support["title"])}" data-summary="{attr(support["lead"])}" aria-labelledby="support-title-{locale_key}">',
        '  <header class="hero">',
        '    <div class="hero-copy">',
        '      <p class="eyebrow">HOWLONG · SUPPORT</p>',
        f'      <h1 id="support-title-{locale_key}">{escape(support["title"])}</h1>',
        f'      <p class="lead">{escape(support["lead"])}</p>',
        "    </div>",
        "  </header>",
        '  <div class="support-main">',
        '    <section class="card email-card">',
        f'      <h2>{escape(support["contactTitle"])}</h2>',
        f'      <p>{escape(support["contact"])}</p>',
        f'      <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>',
        "    </section>",
        '    <section class="card">',
        f'      <h2>{escape(support["faqTitle"])}</h2>',
    ]
    for question, answer in support["faq"]:
        lines.extend([f"      <h3>{escape(question)}</h3>", f"      <p>{escape(answer)}</p>"])
    lines.extend(
        [
            f'      <p class="translation-note">{escape(TRANSLATION_NOTES[locale])}</p>',
            "    </section>",
            "  </div>",
            "</section>",
        ]
    )
    return "\n".join(lines)


def replace_generated_sections(path: Path, marker: str, sections: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(<!-- GENERATED_{marker}_START -->).*?(<!-- GENERATED_{marker}_END -->)",
        re.DOTALL,
    )
    generated = "\n\n".join(sections)
    updated, count = pattern.subn(
        lambda match: f"{match.group(1)}\n{generated}\n        {match.group(2)}",
        content,
        count=1,
    )
    if count != 1:
        raise ValueError(f"Expected one generated-content marker pair in {path}")
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    entries = json.loads((ROOT / "localized-copy.json").read_text(encoding="utf-8"))
    if len(entries) != len(TRANSLATION_NOTES):
        raise ValueError("Each additional locale must have a translated machine-review note")
    locales = [entry["locale"] for entry in entries]
    if len(set(locales)) != len(locales):
        raise ValueError("Duplicate locale in localized-copy.json")
    replace_generated_sections(POLICY_LINK, "POLICY_SECTIONS", [render_policy(entry) for entry in entries])
    replace_generated_sections(SUPPORT_LINK, "SUPPORT_SECTIONS", [render_support(entry) for entry in entries])


if __name__ == "__main__":
    main()
