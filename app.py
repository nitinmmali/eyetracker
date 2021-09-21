
import pixellib
from pixellib.tune_bg import alter_bg
from PIL import Image
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
BACKGROUND_FOLDER ='static/background/background.png/'
BACKGROUND='static/background/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BACKGROUND_FOLDER'] = BACKGROUND_FOLDER
app.config['BACKGROUND'] = BACKGROUND
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # change_bg=alter_bg(model_type='pb')
        # change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
        # #change_bg.change_bg_img(f_image_path=r'D:/Projects/BackgroundRemoval/static//uploads/'+filename , b_image_path=r"D:/Projects/BackgroundRemoval/static//background/background.png", output_image_name=r"D:/Projects/BackgroundRemoval/static/background/"+filename)
        # change_bg.change_bg_img(f_image_path=(app.config['UPLOAD_FOLDER'], filename) , b_image_path="D://Projects//BackgroundRemoval//static//background//background.png", output_image_name=(app.config['BACKGROUND'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        file.save(os.path.join(app.config['BACKGROUND'], filename))
        #print("New filename ="+filename1)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
 
@app.route('/display/<filename>',methods=['POST','GET'])
def display_image(filename):
    #file = request.files['file']
    #filename = secure_filename(file.filename)
    # filename1= "D://Projects//BackgroundRemoval//static//uploads//filename"
    # print("New filename ="+filename1)
    # print(UPLOAD_FOLDER)
        
    
    
    change_bg=alter_bg(model_type='pb')
    change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
    #change_bg.change_bg_img(f_image_path="D://Projects//BackgroundRemoval//image.png",b_image_path="D://Projects//BackgroundRemoval//static//background//background.png",output_image_name="D://Projects//BackgroundRemoval//static//background//imgg.png")
    change_bg.change_bg_img(f_image_path='D://Projects//BackgroundRemoval//static//uploads//'+filename,b_image_path="D://Projects//BackgroundRemoval//static//background//background.png",output_image_name="D://Projects//BackgroundRemoval//static//background//"+filename)
    #change_bg.change_bg_img(f_image_path='//static//uploads//'+filename,b_image_path="//static//background//background.png",output_image_name="//static//background//"+filename)
    # file.save(os.path.join(app.config['BACKGROUND_FOLDER'], filename))
    # print('display_image filename: ' + filename)
    # img1=cv2.imread(filename)
    
    # plt.imshow(filename)
    # plt.show()

    #return redirect(url_for('static', filename='background/' + filename), code=301)
    return redirect(url_for('static', filename='background/' +filename))
 
if __name__ == "__main__":
    app.run(debug=True)