#import "../component/title.typ": approved-and-agreed-fields, signed-field, detailed-sign-field, per-line, student-field
#import "../utils.typ": fetch-field, sign-field

#let arguments(..args, year: auto) = {
  let args = args.named()
  args.organization = fetch-field(
    args.at("organization", default: none),
    default: (
      full: "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ
      ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ «НАЦИОНАЛЬНЫЙ ИССЛЕДОВАТЕЛЬСКИЙ УНИВЕРСИТЕТ
      «ВЫСШАЯ ШКОЛА ЭКОНОМИКИ»
      (НИУ ВШЭ)",
      short: "
      Московский институт электроники и математики им. А.Н.Тихонова",
    ),
    ("*full", "short"),
    hint: "организации",
  )

  args.institute = fetch-field(
    args.at("institute", default: none),
    ("number", "name"),
    default: (number: "", name: ""),
    hint: "института",
  )

  args.department = fetch-field(
    args.at("department", default: none),
    ("number", "name"),
    default: (number: "", name: ""),
    hint: "кафедры",
  )

  args.approved-by = fetch-field(
    args.at("approved-by", default: none),
    ("name*", "position*", "year"),
    default: (year: auto),
    hint: "согласования",
  )
  args.agreed-by = fetch-field(
    args.at("agreed-by", default: none),
    ("name*", "position*", "year"),
    default: (year: auto),
    hint: "утверждения",
  )
  args.stage = fetch-field(
    args.at(
      "stage",
      default: none,
    ),
    ("type*", "num"),
    hint: "этапа",
  )
  args.manager = fetch-field(
    args.at("manager", default: none),
    ("position*", "name*"),
    hint: "руководителя",
  )
  if args.approved-by.year == auto {
    args.approved-by.year = year
  }
  if args.agreed-by.year == auto {
    args.agreed-by.year = year
  }
  return args
}

#let template(
  ministry: "Правительство Российской Федерации",
  organization: (
    full: "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ «НАЦИОНАЛЬНЫЙ ИССЛЕДОВАТЕЛЬСКИЙ УНИВЕРСИТЕТ
    «ВЫСШАЯ ШКОЛА ЭКОНОМИКИ»",
    short: "Московский институт электроники и математики им. А.Н.Тихонова",
  ),
  institute: (number: none, name: none),
  department: (number: none, name: none),
  udk: none,
  research-number: none,
  report-number: none,
  approved-by: (name: none, position: none, year: auto),
  agreed-by: (name: none, position: none, year: none),
  report-type: "Отчёт",
  about: none,
  part: none,
  bare-subject: false,
  research: none,
  subject: none,
  stage: none,
  manager: (position: none, name: none),
  performer: none,
) = {
  grid.cell(align: horizon)[
    #per-line(
      indent: 0pt,
      ministry,
      (value: upper(text(size: 12pt)[#organization.full]), when-present: organization.full),
      (value: text(size: 12pt)[#organization.short], when-present: organization.short),
    )
  ]

  v(1fr)

  per-line(
    align: left,
    (value: [УДК: #udk], when-present: udk),
    (value: [Рег. №: #research-number], when-present: research-number),
    (value: [Рег. № ИКРБС: #report-number], when-present: report-number),
  )


  per-line(
    align: center,
    indent: 1fr,
    (value: upper(report-type), when-present: report-type),
    (value: upper(about), when-present: about),
    "по дисциплине «Основы криптографии и стеганографии»",
    (value: research, when-present: research),
    (value: upper(subject), when-present: subject),
  )

  if performer != none {
    align(right, pad(student-field(performer), left: 20em))
  }
  
  align(right, pad(signed-field(agreed-by), left: 20em))

  v(1.25fr)
}
