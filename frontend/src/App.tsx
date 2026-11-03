import { useEffect, useMemo, useState, type FormEvent } from 'react'
import { SearchIndex, type Excerpt, type Result } from './search'

const SOURCES: Record<string, { title: string; url: string }> = {
  'ubi-regulamento-academico.pdf': { title: 'Regulamento Académico', url: 'https://www.ubi.pt/Ficheiros/Sites/53/Paginas/288/Regulamento%20Acad%C3%A9mico%20da%20UBI.pdf' },
  'ubi-regulamento-creditacao.pdf': { title: 'Regulamento de Creditação', url: 'https://www.ubi.pt/Ficheiros/Sites/53/Paginas/399/Despachos/2022/regulamento_creditacao_ubi.pdf' },
  'ubi-regulamento-propinas.pdf': { title: 'Regulamento de Propinas, alteração de 2020', url: 'https://files.diariodarepublica.pt/2s/2020/02/029000000/0021600225.pdf' },
}
const EXAMPLES = ['Como funciona o exame de recurso?', 'Como posso creditar disciplinas?', 'Quais as prestações das propinas?']

export default function App() {
  const [excerpts, setExcerpts] = useState<Excerpt[] | null>(null)
  const [failed, setFailed] = useState(false)
  const [question, setQuestion] = useState('')
  const [asked, setAsked] = useState('')

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}index.json`)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then(setExcerpts)
      .catch(() => setFailed(true))
  }, [])

  const index = useMemo(() => (excerpts ? new SearchIndex(excerpts) : null), [excerpts])
  const results: Result[] = useMemo(() => (index && asked ? index.search(asked) : []), [index, asked])
  const submit = (e: FormEvent) => { e.preventDefault(); setAsked(question.trim()) }
  const ask = (q: string) => { setQuestion(q); setAsked(q) }

  return (
    <main>
      <p className="eyebrow">Projeto pessoal, sem ligação oficial à UBI</p>
      <h1>Pergunta aos regulamentos da UBI</h1>
      <p className="lead">Encontra os excertos mais relevantes dos regulamentos públicos e mostra sempre o documento e a página.</p>
      <form onSubmit={submit}>
        <label htmlFor="q">A tua pergunta</label>
        <div className="row">
          <input id="q" value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ex.: Como funciona o exame de recurso?" />
          <button disabled={!index || !question.trim()}>Pesquisar</button>
        </div>
      </form>
      <div className="examples">{EXAMPLES.map((q) => <button key={q} type="button" onClick={() => ask(q)}>{q}</button>)}</div>
      {failed && <p role="alert">Não foi possível carregar os documentos. Tenta recarregar a página.</p>}
      {asked && index && results.length === 0 && <p className="empty">Não encontrei isto nos documentos.</p>}
      <ol className="results">
        {results.map(({ excerpt }) => {
          const source = SOURCES[excerpt.documento]
          return (
            <li key={`${excerpt.documento}-${excerpt.pagina}-${excerpt.texto.slice(0, 40)}`}>
              <p>{excerpt.texto}</p>
              <a href={`${source?.url}#page=${excerpt.pagina}`} target="_blank" rel="noreferrer">{source?.title ?? excerpt.documento}, p. {excerpt.pagina}</a>
            </li>
          )
        })}
      </ol>
      <footer>Mostra excertos, não dá aconselhamento. Confirma sempre no documento oficial, porque pode haver versões mais recentes.</footer>
    </main>
  )
}
