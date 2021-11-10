# @ImageJ ij
# @ OpService ops
# @ Img img
# create a new blank image
from jarray import array
#@ output Img projectedX
#@ output Img projectedY
#@ output Img projectedZ


dims = array([150, 100,100], 'l')
blank = ij.op().create().img(dims)

statsOp = ij.op().op("stats.max", blank)

# fill in the image with a sinusoid using a formula
#formula = "10 * (Math.cos(0.3*p[0]) + Math.sin(0.3*p[1]))"

#sinusoid = ij.op().image().equation(blank, formula)
#blank = ops.run("create.img", dims)
img = blank
dims = blank.Dimensions()
#print(dims)
###img.dimensions(dims)
#maxOp = ops.op("stats.max", img)
##
##projectedX = ij.op().run("create.img", dims[1,2])
#
#projectedX = ij.op().create().img([dims[1],dims[2]])
#ops.run("project", projectedX, blank, maxOp, 0)
#projectedX = ij.op().create().img([dims[0],dims[2]])
#ops.run("project", projectedX, blank, maxOp, 1)
#projectedX = ij.op().create().img([dims[0],dims[2]])
#ops.run("project", projectedX, blank, maxOp, 2)
##
##projectedY = ij.op().run("create.img", dims[0,2])
##ij.op().run("project", projectedY, blank, maxOp, 1)
##
##projectedZ = ij.op().run("create.img", dims[0,1])
##ij.op().run("project", projectedZ, img, maxOp, 2)
#
##ij.op().run("project", projected_xy, blank, maxOp, 0)
##ij.op().run("project", projected_yz, blank, maxOp, 1)
##ij.op().run("project", projected_xy, blank, maxOp, 2)
##
##ops.run("project", projectedX, sinusoid, maxOp, 0)
##
##projectedY = ops.run("create.img", dims[0,2])
##ops.run("project", projectedY, sinusoid, maxOp, 1)
##
##projectedZ = ops.run("create.img", dims[0,1])
##ops.run("project", projectedZ, sinusoid, maxOp, 2)
##
##
##
##ij.op
##sinusoid
##
### add a constant value to an image
##ij.op().math().add(sinusoid, 13.0)
##
### generate a gradient image using a formula
##gradient = ij.op().image().equation(ij.op().create().img(dims), "p[0]+p[1]")
##
### add the two images
##composite = ij.op().create().img(dims)
##ij.op().math().add(composite, sinusoid, gradient)
##
### display the images
##ij.ui().show("sinusoid", sinusoid)
##ij.ui().show("gradient", gradient)
##ij.ui().show("composite", composite)