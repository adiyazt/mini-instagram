import PIL.Image
import pilgram
img = PIL.Image.open('static/images/sunrise.jpg')
pilgram.valencia(img).save('static/images/valencia.jpg')
pilgram.willow(img).save('static/images/willow.jpg')
pilgram.brooklyn(img).save('static/images/brooklyn.jpg')
pilgram.gingham(img).save('static/images/gingham.jpg')