from __future__ import division
import numpy as np
import numpy.linalg
import matplotlib as plt
from numpy.linalg import norm


def refract(l, n, n0, n1):
    """
    Given rays with directions l hitting surface normals, n,
    return the refracted directions.
    """
    n /= norm(n, axis=0)[None] # Normalize
    l /= norm(l, axis=0)[None] # Normalize
    costh1 = -(n*l).sum(0)
    sinth2 = (n0/n1) * np.sqrt(1-costh1**2)
    costh2 = np.sqrt(1-sinth2**2)
    if True:
        vrefract = (n0/n1) * l + ((n0/n1) * costh1 - costh2) * n
    else:
        r = n0 / n1
        c = -(n*l).sum(0)
        vrefract = r[None] * l + (r*c * np.sqrt(1-r**2 * (1-c**2)))[None] * n
    return vrefract



class RaytraceSettings(object):
    def __init__(self, clip=True, clipAperture=None):
        self.clip = clip
        if clipAperture is None:
            clipAperture = clip
        self.clipAperture = clipAperture
        

class Glass(object): pass

class SimpleGlass(Glass):
    def __init__(self, n, name=''): 
        self._n = n
        self._name = name
    @property
    def name(self): return self._name    
    def n(self, wavelength): return self._n * np.ones_like(wavelength)
    def __str__(self): return self.name
    def __repr__(self): return '{}({}, {})'.format('SimpleGlass',self.n(0.000555) ,self.name)


class Air(SimpleGlass):
    def __init__(self): 
        SimpleGlass.__init__(self, n=1.0)
    @property
    def name(self): return 'Air'
    def __repr__(self): return '{}()'.format(self.__class__.__name__)

class Surface(object):
    def __init__(self, thickness, glass, semidiam=np.inf):
        self._thickness = thickness
        self._glass = glass
        self._semidiam = semidiam
    def reversed(self, thickness, glass):
        return Surface(thickness, glass, semidiam=self.semidiam)
    def n(self, wavelength): return self._glass.n(wavelength)
    @property
    def glass(self): return self._glass
    @property
    def thickness(self): return self._thickness
    @thickness.setter
    def thickness(self, th): self._thickness = th
    @property
    def semidiam(self): return self._semidiam
    @semidiam.setter
    def semidiam(self, semidiam): self._semidiam = semidiam

    def outline(self):
        """Return z and y points of an outline to draw this."""
        return [0,0], [-self.semidiam, self.semidiam]

    def rayTransferMatrix(self):
        """Return the ray transfer matrix for the thickness."""
        return np.array([[1.0, self.thickness], [0.0, 1.0]])

    def intersectRays(self, z, rays):
        """Compute the points in space where the rays intersect the surface given the surface is at position z.
        Return the points and a mask of valid points."""
        zdist = z - rays.origins[-1]
        result = rays(zdist)
        return result, norm(result[:-1], axis=0) <= self.semidiam
    

class ParaxialSurface(Surface):
    def __init__(self, thickness, f=np.inf, glass=Air(), semidiam=np.inf):
        Surface.__init__(self, thickness=thickness, glass=glass, semidiam=semidiam)
        self._f = f

    def reversed(self, thickness, glass):
        return ParaxialSurface(thickness, f=self.f, glass=glass, semidiam=self.semidiam)

    @property
    def power(self): return 1.0 / self._f

    def rayTransferMatrix(self, n0, wavelength):
        """Return the ray transfer matrix for the given preceeding index and given wavelength."""
        thinRTM = np.array([[1.0, 0.0], [-self.power, 1.0]])
        return Surface.rayTransferMatrix(self).dot(thinRTM)

    def refract(self, z, rays, clip=True):
        origins, mask = self.intersectRays(z, rays)
        directions = np.vstack([rays.directions[:-1] - origins[:-1] * self.power,
                                rays.directions[-1:]])
        if clip:
            directions[:,~mask] = np.nan
        return Rays(origins, directions)
                           
        
class StandardSurface(Surface):
    def __init__(self, thickness, R, glass=Air(), semidiam=np.inf):
        Surface.__init__(self, thickness=thickness, glass=glass, semidiam=semidiam)
        self._R = R

    def reversed(self, thickness, glass):
        return StandardSurface(thickness, R=-self.R, glass=glass, semidiam=self.semidiam)

    @property
    def R(self): return self._R
    @R.setter
    def R(self, R): self._R = R
        
    def outline(self):
        """Return z and y points of an outline to draw this."""
        ys = np.linspace(-self.semidiam, self.semidiam, 30)
        if np.isfinite(self.R):
            z = np.sign(self.R) * np.sqrt(self.R**2 - ys**2)
            return self.R - z, ys
        else:
            return np.zeros_like(ys), ys

    def rayTransferMatrix(self, n0, wavelength):
        """Return the ray transfer matrix for the given preceeding index and given wavelength."""
        n1 = self.n(wavelength)
        refractRTM = np.array([[1.0, 0.0], [(n0-n1)/(self.R * n1), n0/n1]])
        return Surface.rayTransferMatrix(self).dot(refractRTM)


    def intersectRays(self, z, rays):
        if not np.isfinite(self.R):
            return Surface.intersectRays(self, z, rays) # Planar surface.
        l = rays.directions / np.linalg.norm(rays.directions, axis=0)[None]
        o = rays.origins
        c = np.zeros_like(l[:,:1]); c[-1] = z + self.R
        r = self.R
        dp = -(l * (o-c)).sum(0) + np.sqrt((l*(o-c)).sum(0)**2 - np.linalg.norm(o-c,axis=0)**2 + r**2)
        dm = -(l * (o-c)).sum(0) - np.sqrt((l*(o-c)).sum(0)**2 - np.linalg.norm(o-c,axis=0)**2 + r**2)
        d = dm if self.R > 0 else dp
        result = o + l * d
        
        return result, norm(result[:-1], axis=0) <= self.semidiam

    def refract(self, z, rays, clip=True):
        """
        Refract the rays given this lens vertex is at z.
        Return the outgoing rays.
        """
        n0 = rays.n
        n1 = self.n(rays.wavelengths)
        positions, mask = self.intersectRays(z, rays, clip=clip)
        l = rays.directions / norm(rays.directions, axis=0)[None]
        if np.isfinite(self.R):
            c = np.zeros_like(positions[:,:1]); c[-1] = z + self.R
            n = positions - c
        else:
            n = np.zeros_like(positions)
            n[-1] = -1.0
        if self.R < 0 and np.isfinite(self.R): n *= -1
        vrefract = refract(l, n, n0, n1)
        if clip:
            vrefract[:,~mask] = np.nan
        return Rays(positions, vrefract, n=n1)
        

class System(object):
    def __init__(self, surfaces, apertureStop=None, ndim=2):
        self._surfaces = surfaces
        self._apertureStop = apertureStop
        self._ndim = ndim
    def __iter__(self): return iter(self._surfaces)
    def __len__(self): return len(self._surfaces)
    def append(self, *a, **k): return self._surfaces.append(*a, **k)
    
    def reversed(self):
        """Return the reversed system."""
        thkGls = [(S.thickness, S.glass) for S in self.surfaces]
        thkGls = [(0.0, thkGls[-1][1])] + thkGls
        print thkGls
        surfaces = []
        apertureStop = None
        for i, S in enumerate(self.surfaces):
            surfaces.append(S.reversed(*thkGls[i]))
            if S is self.apertureStop:
                apertureStop = surfaces[-1]
        return System(surfaces[::-1], apertureStop=apertureStop)

    @staticmethod
    def loadZMX(zmxfile):
        surfaces = []
        with open(zmxfile, 'r') as fh:
            lines = fh.readlines()
        apertureStop = None
        i = -1
        while i < len(lines) - 1:
            i += 1
            line = lines[i]
            if line.startswith('SURF'):
                isStop = False
                glass = Air()
                while i < len(lines) - 1:
                    i += 1
                    line = lines[i]
                    if 'STOP' in line:
                        isStop = True
                    if 'TYPE STANDARD' in line or 'TYPE EVENASPH' in line:
                        ctor = StandardSurface
                    if 'CURV' in line:
                        curv = float(line.split()[1])
                        R = 1.0 / curv if curv != 0 else np.inf
                    if 'DIAM' in line:
                        semidiam = float(line.split()[1]) / 2.0
                        if semidiam < 0.1: semidiam = 5.0
                    if 'DISZ' in line:
                        thickness = float(line.split()[1])
                    if 'GLAS' in line:
                        parts = line.split()
                        glass = SimpleGlass(float(parts[4]), name=parts[1])
                    if not line.startswith(' '):
                        i -= 1
                        try:
                            surfaces.append(ctor(thickness=thickness, R=R, glass=glass, semidiam=semidiam))
                            if isStop:
                                apertureStop = surfaces[-1]
                        except Exception as e:
                            print ctor, e
                            import epdb; epdb.st()
                        break
                        
        return System(surfaces, apertureStop=apertureStop)
    @property
    def surfaces(self): return self._surfaces
    #@property
    #def z0(self):
    #    """The z position of surface zero."""
    #    return 0.0
    @property
    def ndim(self):
        """Number of spatial dimentions."""
        return self._ndim
    def unitVec(self, dim, *a, **k):
        """A unit vector in the given direction: Useful for dealing with 2 or 3 dimensions interchangably."""
        result = np.zeros(self.ndim, *a, **k)
        result[dim] = 1
        return result
    def unitCol(self, dim, *a, **k):
        """A unit column vector in the given direction."""
        return self.unitVec(dim, *a, **k)[:,None]

    @property
    def surfaceVertices(self):
        """Return the position of all surfaces."""
        zOffset = 0.0 #self.z0
        if not np.isfinite(self.surfaces[0].thickness):
            zs = np.hstack([[-np.inf, 0.0], 
                                np.cumsum([S.thickness for S in self._surfaces[1:-1]])])
        else:
            zs = zOffset + np.cumsum(np.hstack([[0.0], [S.thickness for S in self._surfaces[:-1]]]))
        result = np.zeros((self.ndim, len(zs)))
        result[-1] = zs
        return result
    @property
    def apertureStop(self): return self._apertureStop
    
    def rayTransferMatrix(self, wavelength=None):
        TM = np.eye(2)
        if not self.surfaces: return TM # No surfaces
        n = self.surfaces[0].n(wavelength)
        for surface in self._surfaces:
            TM = surface.rayTransferMatrix(n, wavelength).dot(TM)
        return TM
            
    def marginalRayAngleRTM(self, fieldzy, wavelength=None):
        """Compute the angle to graze the edge of the pupil."""
        apInd = self.surfaces.index(self.apertureStop)
        RTM = System(self.surfaces[:apInd]).rayTransferMatrix(wavelength)
        stopy = self.apertureStop.semidiam
        # Now solve for theta_0: [[stopy],[theta_i]] = RTM.dot([[fieldy],[theta_0]])
        RTM = RTM.dot([[1,fieldzy[0]],[0,1]]) # Shift so we start at zero.
        theta_0 = (stopy - RTM[0,0] * fieldzy[1]) / RTM[0,1]
        return theta_0

    def marginalRayAngle(self, fieldPoint, wavelength=None, eps=1e-5):
        """Compute the angle to graze the edge of the pupil."""
        apInd = self.surfaces.index(self.apertureStop)
        frontSys = System(self.surfaces[:apInd+1])
        stopy = self.apertureStop.semidiam
        def residual(theta, stopy):
            """Compute the residual of hitting the top edge of the aperture."""
            if not np.isscalar(theta): theta = theta.flatten()[0] # Make theta be a scalar.
            direction = np.zeros((self.ndim, 1));
            direction[-2:,0] = [np.tan(theta), 1.0]
            ray = Rays(np.reshape(fieldPoint, (-1,1)), direction, wavelength=wavelength)
            pts, rayOut = frontSys.cast(ray, settings=RaytraceSettings(False))
            #import pdb;pdb.set_trace()
            #print '[{},{}],'.format(theta, rayOut.origins[-2,0] - stopy),
            result = rayOut.origins[-2,0] - stopy
            if np.isnan(result): result = np.inf
            return result
        def residFudged(theta, stopy):
            return residual(theta, stopy) + eps * stopy
        from scipy.optimize import fmin, bisect
        theta0 = self.marginalRayAngleRTM(fieldPoint[-2:][::-1], wavelength)
        results = [None, None]
        for i, pm1 in enumerate((-1, 1)):
            if True:
                try:
                    results[i] = bisect(residFudged, pm1 * 0.5 * theta0, pm1 * 1.5 * theta0, args=(pm1 * stopy,))
                except ValueError:
                    pass
            if results[i] is None:
                thetas = np.pi * 0.1 * np.linspace(-1, 1, 21)
                resids = np.array([residFudged(theta, pm1*stopy) for theta in thetas])
                th0 = thetas[np.argmin(resids**2)]
                mask = np.isfinite(resids)
                #print 'thetas', thetas
                #print 'resids', resids
                resids = resids[mask]
                thetas = thetas[mask]
                try:
                    pos = thetas[resids > 0][np.argmin(resids[resids > 0])]
                    neg = thetas[resids < 0][np.argmax(resids[resids < 0])]
                except ValueError:
                    # We can get here if the lens focuses all points at this field point to the same point at the aperture plane.
                    raise
                #print '------'
                #print pos, residFudged(pos, pm1*stopy), resids[resids > 0][np.argmin(resids[resids > 0])]
                #print neg, residFudged(neg, pm1*stopy), resids[resids < 0][np.argmax(resids[resids < 0])]
                try:
                    results[i] = bisect(residFudged, pos, neg, args=(pm1 * stopy,))
                except ValueError:
                    results[i] = fmin(lambda *a: residFudged(*a)**2, x0=np.mean(thetas), args=(pm1 * stopy,))[0]
                    print 'resid:',results[i], residFudged(results[i], pm1*stopy)
        return results
    
    def marginalRayPositions(self, direction, wavelength=None, eps=1e-5):
        """Compute positions for the marginal rays that have the given direction."""
        front = self[:self.surfaces.index(self.apertureStop)+1].reversed()
        pts, rays = front.cast(Rays([[0],[front.apertureStop.semidiam-eps]], -np.reshape(direction, (-1,1))), clip=False)
        direction /= norm(direction, axis=0)
        from scipy.optimize import fmin, bisect
        def residualAndInfo(aperatureDirection, stopPos, clip=False):
            apdir = np.reshape(aperatureDirection, (-1,1))
            apdir /= norm(apdir)
            pts, rays = front.cast(Rays(stopPos, apdir), clip=clip)
            print 'appdir ,dir'
            #print apdir.flatten()
            #print rays.directions.flatten()
            print rays.directions.flatten() - direction.flatten()
            return rays.directions.flatten() - direction, pts, rays
        def residual(aperatureDirection, stopPos, clip=False):
            # Smoothly penalize slopes beyond +/-badSlope
            badSlope = 1.0
            penalty = (np.clip(norm(aperatureDirection[:-1], axis=0) / aperatureDirection[-1], badSlope, np.inf) - badSlope)**2 + 1
            result, pts, rays = residualAndInfo(aperatureDirection, stopPos, clip=clip)
            if np.any(np.isnan(result)):
                import pdb;pdb.set_trace()
                result = np.inf
                #result, pts, rays = residualAndInfo(aperatureDirection, stopPos, clip=clip)
            print penalty, result, aperatureDirection
            return norm(result) * penalty # + (np.linalg.norm(aperatureDirection) - 1)**2 # Also penalize non-unity direction vectors.
            #return  penalty * (np.linalg.norm(aperatureDirection) - 1)**2 # Also penalize non-unity direction vectors.


        #def inOrOut(aperatureDirection, stopPos):
        #    return np.cast[float](~np.isnan(residual(aperatureDirection, stopPos, clip=True))) - 0.5
        stopEdges = (self.unitCol(-2) *  -(front.apertureStop.semidiam-eps),
                     self.unitCol(-2) *   (front.apertureStop.semidiam-eps))
        results = [fmin(lambda y: residual([0.0] * (self.ndim-2) + [y, 1], stopEdge), [0])[0] for stopEdge in stopEdges]
        results = np.array([self.unitVec(-2) * y + self.unitVec(-1) for y in results]) # Make it have the right shape, with optional x then a y and z=1.0.
        import pdb;pdb.set_trace()
        return results
            
        
    def marginalRays(self, fieldPoint, wavelength=None):
        if isinstance(fieldPoint, FieldHeight):
            return self.marginalRayAngle(fieldPoint.point)
        elif isinstance(fieldPoint, FieldAngle):
            positions = self.marginalRayPositions(self.unitVec(-2) * np.tan(fieldPoint.theta) + self.unitVec(-1), wavelength)
            import pdb;pdb.set_trace()
            raise NotImplemented()

    def __getitem__(self, *a ,**k):
        return System(self._surfaces.__getitem__(*a, **k), apertureStop=self.apertureStop)
    def outlines(self):
        tops = []
        bottoms = []
        isGlass = 1.0 != np.array([s.n(None) for s in self.surfaces])
        from scipy.ndimage import shift
        drawEdge = np.logical_or(isGlass, shift(isGlass, 1, order=0))
        for pt, surface, drawFrom, drawTo in zip(self.surfaceVertices[-2:].T, self._surfaces, 
                                                  isGlass, shift(isGlass,1,order=0)):
            ctr = pt[::-1][:,None] # y then z components in a column.
            outline = ctr + surface.outline()
            if drawFrom or drawTo:
                tops.append(outline[:,-1])
                bottoms.append(outline[:,0])
            if not drawFrom:
                tops.append([np.nan,np.nan])
                bottoms.append([np.nan,np.nan])
            if surface is self.apertureStop:
                y = surface.semidiam
                sz = y * 0.1
                yield ctr + (np.array([0, sz, -sz, 0, np.nan, 0, sz, -sz, 0]),
                             np.array([y, y+sz, y+sz, y, np.nan, -y, -y-sz, -y-sz, -y]))
                if drawFrom or drawTo:
                    yield outline # Outline the stop only if it's got power.
            else:
                yield outline

        yield np.transpose(tops)
        yield np.transpose(bottoms)
                
    def cast(self, rays, settings=RaytraceSettings()):
        """Cast the rays through the system.
        Return the sequence of lines and the resulting output rays."""
        assert self.ndim == rays.ndim
        points = [rays.origins]
        for z, S in zip(self.surfaceVertices[-1], self.surfaces):
            clip = settings.clip if S is not self.apertureStop else settings.clipAperture
            rays = S.refract(z, rays, clip=clip)
            points.append(rays.origins)
        return np.array(points), rays
            

class FieldPoint(object):
    pass

class FieldHeight(object):
    def __init__(self, pt):
        self._pt = np.array(pt, dtype=float)
    @property
    def point(self): return self._pt
    def makeRays(self, system, n=3, wavelength=None):
        """Given a system, make a ray bundle with n rays."""
        rayslopes = np.tan(system.marginalRays(self, wavelength=wavelength))
        rays = Rays(self.point[:,None] * np.ones(n),
                    (system.unitCol(-2) * np.linspace(rayslopes[0], rayslopes[1], n) +
                     system.unitCol(-1) * np.ones(n)))
        return rays

class FieldAngle(object):
    def __init__(self, theta):
        self._theta = theta
    @property
    def theta(self): return self._theta
    def makeRays(self, system, n=3, wavelength=None):
        """Given a system, make a ray bundle with n rays."""
        rayslope = np.tan(-fieldTheta)
        fieldHeights = system.marginalRays(self, wavelength)
        rays = Rays(system.unitCol(-2) * np.linspace(fieldHeights[0], fieldHeights[1], n),
                    (system.unitCol(-2) * np.ones(n) * rayslope +
                     system.unitCol(-1) * np.ones(n)))
        return rays
        
    
class Rays(object):
    """
    A collection of rays of the given wavelengths in the given index medium.
    """
    def __init__(self, origins, directions, n=1.0, wavelength=None):
        origins = np.array(origins, dtype=float)
        directions = np.array(directions, dtype=float)
        assert origins.shape[0] in (2, 3), "Must be row vectors."
        assert origins.shape == directions.shape
        self._origins = origins
        self._directions = directions / directions[-1:] # Normalize so z componenet is unity.
        if np.size(n) == 1:
            n = n * np.ones_like(origins[-1])
        self._n = n
    @staticmethod
    def combine(*rays):
        return Rays(np.hstack([r.origins for r in rays]),
                    np.hstack([r.directions for r in rays]))
    def __call__(self, dz):
        return self.origins + dz * self.directions
    @property
    def origins(self): return self._origins
    @property
    def directions(self): return self._directions
    @property
    def n(self): 
        return self._n
    @property
    def wavelengths(self):
        return 0.0005 * np.ones_like(self.origins[-1])
    @property
    def ndim(self): 
        """Number of spatial dimensions."""
        return len(self.origins)
