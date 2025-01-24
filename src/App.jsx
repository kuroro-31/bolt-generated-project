import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await axios.post('/api/summarize', { url })
      setSummary(response.data.summary)
    } catch (error) {
      console.error(error)
      setSummary('Error fetching summary')
    } finally {
      setLoading(false)
    }
  }

  return (
    &lt;div className="container"&gt;
      &lt;h1&gt;YouTube Video Summarizer&lt;/h1&gt;
      &lt;form onSubmit={handleSubmit}&gt;
        &lt;input
          type="text"
          value={url}
          onChange={(e) =&gt; setUrl(e.target.value)}
          placeholder="Enter YouTube URL"
          required
        /&gt;
        &lt;button type="submit" disabled={loading}&gt;
          {loading ? 'Summarizing...' : 'Get Summary'}
        &lt;/button&gt;
      &lt;/form&gt;
      {summary && (
        &lt;div className="summary"&gt;
          &lt;h2&gt;Summary&lt;/h2&gt;
          &lt;p&gt;{summary}&lt;/p&gt;
        &lt;/div&gt;
      )}
    &lt;/div&gt;
  )
}

export default App
