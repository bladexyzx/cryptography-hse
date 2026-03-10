#import "../utils.typ": fetch-field, unbreak-name
#import "performers.typ": performers-page

#let detailed-sign-field(title, name, position, year) = {
    assert(type(name) == str, message: "Некорректный тип поля name в detailed-sign-field, должен быть строкой")
    assert(type(position) == str, message: "Некорректный тип поля position в detailed-sign-field, должен быть строкой")
    assert(type(year) in (int, type(none)), message: "Некорректный тип поля year в detailed-sign-field, должен быть целым числом")
    let year-cell = []
    let line-end = 7
    if year != none {
      year-cell = table.cell(align: right)[#year г.]
      line-end = 6
    }
    table(
        stroke: none,
        align: left,
        inset: (x: 0%),
        columns: (8pt, 2fr, 2pt, 10pt, 2fr, auto, 45pt),
        table.cell(colspan: 7)[#title],
        table.cell(colspan: 7)[#position],
    )
    block(spacing: 0pt)[
      #table(
        stroke: none,
        align: left,
        inset: (x: 0%),
        columns: (5pt, 23pt, 5pt, 70pt, 35pt, 100pt),
        table.cell(colspan: 4)[], table.cell(colspan: 2, align: left)[#unbreak-name(name)],
        table.hline(start: 0, end: 4),
        table.cell(align: left)[«], [], table.cell(align: right)[»], [], table.cell(colspan: 1, align: left)[#year-cell],
        table.hline(start: 1, end: 2),
        table.hline(start: 3, end: 4)
      )
    ]
}

#let align-function = align

#let per-line(align: center, indent: 1fr, force-indent: false, ..values) = {
  let result = ()
  for value in values.pos() {
    let rule = false
    if type(value) in (array, dictionary) {
      let data = fetch-field(value, ("value*", "when-rule", "when-present", "rule"), default: (when-present: "always", when-rule: "always", rule: array.all), hint: "линии")
      assert(not (data.when-rule != "always" and data.when-present != "always"), message: "Должно быть выбрано только одно правило пояивления when-rule или when-present")
      if data.when-rule != "always" {
        rule = data.when-rule
      }
      if data.when-present != "always" {
        rule = (data.rule)((data.when-present, ).flatten(), elem => elem != none)
      }
      if data.when-rule == "always" and data.when-present == "always" {
        rule = true
      }
      value = data.value
    } else {
      rule = value != none
    }
    if rule {
      result.push(value)
    }
  }

  if result != () {
    align-function(align)[
      #grid[#for elem in result {[#elem \ ]}]
    ]
  }
  if force-indent or result != () {
    v(indent)
  }
}

#let if-present(rule: array.all, indent: v(1fr), ..targets, body) = {
  assert(rule in (array.all, array.any), message: "Правило сравнения указано неверно, должно быть array.all или array.any")
  let check = (target => target != none)
  if rule(targets.pos(), check) {
    body
    indent
  }
}

#let approved-field(approved-by) = {
  if approved-by.name != none [
    #detailed-sign-field("согласовано", approved-by.name, approved-by.position, approved-by.year)
  ]
}

#let signed-field(agreed-by) = {
  if agreed-by.name != none [
    #detailed-sign-field("Руководитель", agreed-by.name, agreed-by.position, agreed-by.year)
  ]
}

#let student-field(performer) = {
  if performer.name != none [
    #detailed-sign-field("", performer.name, performer.position, 2026)
  ]
}

#let approved-and-agreed-fields(approved-by, agreed-by) = {
  if-present(rule: array.any, approved-by.name, agreed-by.name)[
    #grid(
      columns: (1fr, 1fr),
      align: (left, right),
      gutter: 15%,
      approved-field(approved-by),
      agreed-field(agreed-by)
    )
  ]
}
