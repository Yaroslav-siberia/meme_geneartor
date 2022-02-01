  const GeneratorEndpoint = "generate"
  const loadingSrc = "../static/images/loader.gif"
  const resultImage = document.getElementById("result-image")
  const downloadBtn = document.getElementById("downloadBtn")

  const template_ids = ["102156234", "8072285", "99683372", "259237855", "195515965", "922147", "155067746","114585149","61539"];
  const all_template_ids = ["102156234", "8072285", "99683372", "259237855", "195515965", "922147", "155067746","114585149","61539",
                          "188390779","155067746","87743020","119139145","112126428","178591752","131087935","196652226","134797956",
                          "28251713","27813981","100777631","114585149","175540452","84341851","132769734","93895088","129242436",
                          "102156234","181913649","135256802","16464531","184801100","3218037","170715647","163573","61581","74191766",
                          "124822590","438680","1035805","89370399","40945639","61733537","164335977","10364354","326093",
                          "4087833","135678846","61520","217743513","134797956","222403160","148909805","226297822"]

const template_dict = {
   "102156234":"Mocking-Spongebob",
   "8072285": "Doge",
   "99683372": "Sleeping-Shaq",
   "259237855":"Laughing-Leo",
   "195515965":"Clown-Applying-Makeup",
   "922147":"Laughing-Men-In-Suits",
   "155067746":"Surprised-Pikachu",
   "114585149": "Inhaling-Seagull",
   "61539": "First-World-Problems"
  }                          
  
  function generate_random_meme(){
      const random = Math.floor(Math.random() * template_ids.length);
      resultImage.src = loadingSrc
      fetch(`${GeneratorEndpoint}/${template_ids[random]}`)
          .then(res => res.json())
          .then(data => resultImage.src = data.user_image)
      downloadBtn.disabled = false;
  }
  function generate_meme_by_id(id, user_input){
      
      
      resultImage.src = loadingSrc
      fetch(`${GeneratorEndpoint}/${id}?text=${user_input}`)
          .then(res => res.json())
          .then(data => resultImage.src = data.user_image)
      console.log(resultImage.src);
      downloadBtn.disabled = false;
  }
  
  async function download_image(){
      var downloadImage = document.getElementById("result-image");
      const image = await fetch(downloadImage.src)
      const imageBlog = await image.blob()
      const imageURL = URL.createObjectURL(imageBlog)

      const link = document.createElement('a')
      link.href = imageURL
      link.download = downloadImage.title
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
  }