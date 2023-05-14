import React from 'react'
import './footer.css'

const Footer = (): JSX.Element => {
  const githubHTML = '<i class="devicon-github-original-wordmark"></i>'
  const linkedinHTML = '<i class="devicon-linkedin-plain"></i>'
  const gmailHTML = '<i class="devicon-google-plain"></i>'

  return (
    <div className="othello_footer">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.15.1/devicon.min.css"/>
      <h3> Aditya Kak </h3>
      <div className="othello_footer_row">
        <div className="othello_footer_column">
          <a href='https://github.com/adityakak/othello'>
            <div dangerouslySetInnerHTML={{ __html: githubHTML }} style={{ fontSize: '2vw' }} />
          </a>
        </div>
        <div className="othello_footer_column">
          <a href='https://www.linkedin.com/in/adityakak/'>
            <div dangerouslySetInnerHTML={{ __html: linkedinHTML }} style={{ fontSize: '2vw' }} />
          </a>
        </div>
        <div className="othello_footer_column">
          <a href='mailto:adityakak04@gmail.com'>
            <div dangerouslySetInnerHTML={{ __html: gmailHTML }} style={{ fontSize: '2vw' }} />
          </a>
        </div>
      </div>
    </div>
  )
}

export default Footer
