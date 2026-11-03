export interface Excerpt { documento: string; pagina: number; texto: string }
export interface Result { score: number; excerpt: Excerpt }

const STOP = new Set('a ao aos as com como da das de do dos e em na nas no nos o os ou para pela pelo por que se um uma quando qual quais posso pode'.split(' '))
const SUFFIXES = ['acoes', 'acao', 'adores', 'ador', 'ados', 'adas', 'ado', 'ada', 'ando', 'endo', 'arem', 'ar', 'er', 'ir', 'am', 'em', 'as', 'es', 'os', 'a', 'e', 'o', 's']
const K1 = 1.5
const B = 0.75

/** Reduz uma palavra à raiz, para "creditar" e "creditação" coincidirem. */
export function stem(word: string): string {
  for (const suffix of SUFFIXES) {
    if (word.endsWith(suffix) && word.length - suffix.length >= 4) return word.slice(0, -suffix.length)
  }
  return word
}

export function tokenize(text: string): string[] {
  const clean = text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/-\s+/g, '')
  return (clean.match(/[a-z0-9]+/g) ?? []).filter((t) => !STOP.has(t)).map(stem)
}

export class SearchIndex {
  private readonly counts: Map<string, number>[]
  private readonly lengths: number[]
  private readonly average: number
  private readonly presence = new Map<string, number>()
  private readonly excerpts: Excerpt[]

  constructor(excerpts: Excerpt[]) {
    this.excerpts = excerpts
    this.counts = excerpts.map((e) => {
      const count = new Map<string, number>()
      for (const t of tokenize(e.texto)) count.set(t, (count.get(t) ?? 0) + 1)
      return count
    })
    this.lengths = this.counts.map((c) => [...c.values()].reduce((a, b) => a + b, 0))
    this.average = this.lengths.reduce((a, b) => a + b, 0) / Math.max(this.lengths.length, 1)
    for (const c of this.counts) for (const t of c.keys()) this.presence.set(t, (this.presence.get(t) ?? 0) + 1)
  }

  search(question: string, limit = 5): Result[] {
    const terms = [...new Set(tokenize(question))]
    const total = this.excerpts.length
    return this.excerpts
      .map((excerpt, i) => {
        let score = 0
        let matched = 0
        for (const term of terms) {
          const freq = this.counts[i].get(term) ?? 0
          if (!freq) continue
          matched += 1
          const n = this.presence.get(term) ?? 0
          const idf = Math.log(1 + (total - n + 0.5) / (n + 0.5))
          score += (idf * freq * (K1 + 1)) / (freq + K1 * (1 - B + (B * this.lengths[i]) / this.average))
        }
        // Favorece excertos que cobrem mais termos da pergunta.
        return { score: score * (matched / Math.max(terms.length, 1)), excerpt }
      })
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
  }
}
