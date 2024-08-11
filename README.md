
# Curvetopia: A Journey into the World of Curves

This project uses cutting edge mathematical algorithms and optimized computer graphics techniques to carrye out regularization, symmetry analysis and occlusion infilling in hand-drawn shapes and doodles. All the code for this project was written from 25th of July to 11th of August, as a submission to Adobe Gensolve Hackathon Round-2.  

**Please visit the jupyter notebooks to view the mathematics and code behind our algorithms**

### Regularization and Symmetry

We have adhered to using traditional mathematical algorithms and computer graphics techniques to correct and regularize shapes, detect the presence of regular shapes inside a plot and to detect axes of symmetry across the regularized plot. We have largely utilized the properties of the cubic bezier curves and focused on contemporary optimization tactics using data structures such as **optimal-heap** and **low-latency undirected graphs** to tackle complexity issues.

The most important highlight for this section is out custom optimization on the **Ramer-Douglas-Peucker** algorithm and **Johnson's algorithm**, which has reduced these steps to a complexity of **O(n*logn)**.

We deployed this into a web-app, to test the generalizaion and performance of our algorithms on hand-drawn doodles. Please visit it using this link: [Curvetopia: A Journey into the World of Curves](https://curvotopia.vercel.app/). Here are some snapshots.
#### Before Regularization
![Before Regularization](https://github.com/user-attachments/assets/87f88f24-2bd5-4067-a25d-4dfc3941993b)

#### After Regularization
![After Regularization](https://github.com/user-attachments/assets/485cd30a-b162-4381-99ec-df1bc75b48ea)

### Completing the Incomplete curves

We have adhered to traditional geometry and computer graphics algorithms to fill in occluded portions with a **single cubic bezier curve**. Our approach has been to first obtain an SVG by Bezier interpolation from CSV point mappings, and then building the infilling algorithm on the basis of corner points.  

Unlike several other redundant solutions that use deep learning and computer vision techniques for this, we have used the inherent properties of bezier curves, specifically the **centres of the osculating circles**. We developed a cross-link converging interpolation technique that estimates the control points of the infilling curve using the surrounding osculating circle centres.

Here are some snapshots.

#### First TestCase 
![First TestCase](https://github.com/user-attachments/assets/3f395941-7dbe-46a3-84df-b6e752bcf80b)

#### Second TestCase
![Second TestCase](https://github.com/user-attachments/assets/d59c1b9b-3419-40d2-b763-e31e0b14a4ba)

## Authors

- [Shubham Shinde](https://www.linkedin.com/in/shubhamshinde6762/)

- [Aarya Bhave](https://www.linkedin.com/in/aarya-bhave-aa4a13256/)

