import util
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')

def welcome():
    return render_template('form.html')


@app.route('/result', methods = ['POST'])

def result():
    water = util.tube()
    naphtha = util.shell()
    sthe = util.process()
    
    water.Tin= request.form.get("TubeTin", type=float)
    water.Tout = request.form.get("TubeTout", type= float)
    water.ro = request.form.get("Tubero", type= float)
    water.Cp = request.form.get("TubeCp", type= float)
    water.mu = request.form.get("Tubemu", type= float)
    water.K = request.form.get("TubeK", type= float)
    water.Rf = request.form.get("TubeRf", type= float)
    water.Pr = request.form.get("TubePr", type= float)
    water.w = request.form.get("Tubew", type= float)
    water.Ft = request.form.get("Ft", type= float)

    naphtha.Tin= request.form.get("ShellTin", type=float)
    naphtha.Tout = request.form.get("ShellTout", type= float)
    naphtha.ro = request.form.get("Shellro", type= float)
    naphtha.Cp = request.form.get("ShellCp", type= float)
    naphtha.mu = request.form.get("Shellmu", type= float)
    naphtha.K = request.form.get("ShellK", type= float)
    naphtha.Rf = request.form.get("ShellRf", type= float)
    naphtha.Pr = request.form.get("ShellPr", type= float)
    naphtha.w = request.form.get("Shellw", type= float)

    util.design(naphtha, water)

    return render_template('results.html', water = water, naphtha = naphtha)
    

if(__name__ == '__main__'):
    app.run(debug = True)
    

#naphtha = util.shell()
#water = util.tube()