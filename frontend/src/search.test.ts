import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { SearchIndex, tokenize, type Excerpt } from './search'

const excerpts: Excerpt[] = JSON.parse(readFileSync('public/index.json', 'utf-8'))
const index = new SearchIndex(excerpts)

describe('tokenize', () => {
  it('junta variantes da mesma palavra', () => {
    expect(tokenize('creditar')).toEqual(tokenize('creditação'))
  })
})

describe('perguntas reais', () => {
  const cases: [string, string, RegExp][] = [
    ['Quantas vezes posso fazer exame de recurso?', 'ubi-regulamento-academico.pdf', /exame de recurso/i],
    ['Como posso creditar disciplinas de outro curso?', 'ubi-regulamento-creditacao.pdf', /credita/i],
    ['Quais as prestações das propinas?', 'ubi-regulamento-propinas.pdf', /presta/i],
    ['O que é a época de recurso?', 'ubi-regulamento-academico.pdf', /recurso/i],
  ]
  it.each(cases)('%s', (question, documento, text) => {
    const top = index.search(question, 3).map((r) => r.excerpt)
    expect(top.some((e) => e.documento === documento && text.test(e.texto))).toBe(true)
  })
  it('o primeiro resultado de creditação vem do documento certo', () => {
    expect(index.search('Como posso creditar disciplinas?')[0].excerpt.documento).toBe('ubi-regulamento-creditacao.pdf')
  })
  it('não inventa resultados', () => {
    expect(index.search('xilofone')).toEqual([])
  })
})
