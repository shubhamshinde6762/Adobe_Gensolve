---

# Curvetopia: A Journey into the World of Curves

This project uses cutting-edge mathematical algorithms and optimized computer graphics techniques to carry out regularization, symmetry analysis, and occlusion infilling in hand-drawn shapes and doodles. All the code for this project was written from 25th of July to 11th of August, as a submission to Adobe Gensolve Hackathon Round-2.

**Please visit the Jupyter notebooks to view the mathematics and code behind our algorithms.**

### Regularization and Symmetry

We have adhered to using traditional mathematical algorithms and computer graphics techniques to correct and regularize shapes, detect the presence of regular shapes inside a plot, and to detect axes of symmetry across the regularized plot. We have largely utilized the properties of the cubic Bézier curves and focused on contemporary optimization tactics using data structures such as **optimal-heap** and **low-latency undirected graphs** to tackle complexity issues.

The most important highlight of this section is our custom optimization of the **Ramer-Douglas-Peucker** algorithm and **Johnson's algorithm**, which has reduced these steps to a complexity of **O(n*logn)**.

We deployed this into a web app to test the generalization and performance of our algorithms on hand-drawn doodles. Please visit it using this link: [Curvetopia: A Journey into the World of Curves](https://curvotopia.vercel.app/). Here are some snapshots:


- **Before Regularization:** ![Before Regularization](https://github.com/user-attachments/assets/87f88f24-2bd5-4067-a25d-4dfc3941993b)

  
- **After Regularization:** ![After Regularization](https://github.com/user-attachments/assets/485cd30a-b162-4381-99ec-df1bc75b48ea)


Here are the outputs for the given testcases:


- **frag0:** ![frag0](https://github.com/user-attachments/assets/48a62eb9-1d79-47d2-8e9a-f79f5ea21462)


- **frag1:** ![frag1](https://github.com/user-attachments/assets/7dd39f82-c8eb-40d9-bf56-49d735d26031)


- **frag2:** ![frag2](https://github.com/user-attachments/assets/ceeeffd6-cbd7-4fcc-a523-20ccf4709f9d)


- **isolated:** ![isolated](https://github.com/user-attachments/assets/f5b760e3-674c-484f-9c70-3941e9499eec)


For more details, visit our [Regularization and Symmetry Analysis Colab Notebook](https://colab.research.google.com/drive/1fYRGmyuaJPW4emlv6oFc5tRacVraONJz?usp=sharing) page.

### Completing the Incomplete Curves

We have adhered to traditional geometry and computer graphics algorithms to fill in occluded portions with a **single cubic Bézier curve**. Our approach has been to first obtain an SVG by Bézier interpolation from CSV point mappings, and then build the infilling algorithm based on corner points.

Unlike several other redundant solutions that use deep learning and computer vision techniques for this, we have used the inherent properties of Bézier curves, specifically the **centers of the osculating circles**. We developed a cross-link converging interpolation technique that estimates the control points of the infilling curve using the surrounding osculating circle centers.

Here are some snapshots:

- **First Test Case:** ![First Test Case](https://github.com/user-attachments/assets/3f395941-7dbe-46a3-84df-b6e752bcf80b)
- **Second Test Case:** ![Second Test Case](https://github.com/user-attachments/assets/d59c1b9b-3419-40d2-b763-e31e0b14a4ba)

For more details, visit our [Occlusion Infilling Colab Notebook](https://colab.research.google.com/drive/1ZzidTt0xzyM3Js9-QK43d8cv_bvI4tlX?usp=sharing) page.

## Authors

- [Shubham Shinde](https://www.linkedin.com/in/shubhamshinde6762/)
- [Aarya Bhave](https://www.linkedin.com/in/aarya-bhave-aa4a13256/)

--- 
