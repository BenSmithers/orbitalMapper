# orbitalMapper


For camera vector \vec{c} and planet vector \vec{p}, we know the vector pointing to the planet from the camera is \vec{p}-\vec{c}. So then we can solve for the angles. 

The angle away would be \arccos( p\cdot c / (\abs{p} \abs{c})). This is the angle away from the focus

Then we project the difference vector onto the plane defined by a normal vector \vec{c}, normalized. And find the angular difference between that the z-axis projected onto the same plane. 

This is the angle from the vertical in our projection 

OH I should also pre-compute the orbital trajectories on launch and store them in the objects. Maybe 200-300 points (with extra on the ends). Then we do a bilinear (or quadratic :thinking:) interpolation
