import axios from 'axios'


const getData = async (jsonData) => {
    let data = {}
    await axios.post('http://127.0.0.1:8000/data', jsonData)
        .then(res => {
            data = res.data

        }).catch(e => {
            console.log(e.message)
    })
    return data
}

export default getData

