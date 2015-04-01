#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports
import math, cmath
from . import tkgame_animations as AP



class Physics:
    """
        Physics path management;
    """

    def __del__ (self):
        """
            free references before dying;
        """
        self.animations.release(
            self._computation_loop,
            self.update_callback,
        )
    # end def


    def __init__ (self, **kw):
        """
            class constructor;
        """
        # member inits
        self.animations = AP.get_animation_pool()
        self.started = False
        self.velocity = None
        self.friction = 0.0
        self.gravity = kw.get("gravity") or 9.8
        self.framerate = kw.get("framerate") or 20
        self.update_callback = kw.get("on_frame_update")
    # end def


    def _computation_loop (self, *args, **kw):
        """
            main physics computation loop;
        """
        # parabolic path (in derived mode, dV/dt)
        # i.e.  Vx = Vx * (1 - f * dt)  (ground friction)
        #       Vy = Vy - g * dt        (vertical gravity)
        self.velocity.x *= (1.0 - self.friction * self.dt)
        self.velocity.y -= self.gravity * self.dt
        # call frame update (deferred)
        self.animations.run_after_idle(
            # closure for self.update_callback
            self.update_closure(
                dx=self.velocity.x,
                dy=self.velocity.y,
                dt=self.dt
            )
        )
        # loop again
        self.animations.run_after(self.delay, self._computation_loop)
    # end def


    def apply_new (self, **kw):
        """
            applies new keyword arguments to body's current path;
        """
        # inits
        self.velocity = kw.get("velocity", self.velocity)
        self.friction = kw.get("friction", self.friction)
        # start physics (if not already done)
        self.start()
    # end def


    @property
    def framerate (self):
        """
            attribute property: number of computation frames per second
            to take in account (integer, 1-20);
        """
        return self.__framerate
    # end def

    @framerate.setter
    def framerate (self, value):
        # set value
        self.__framerate = max(1, min(20, int(value)))
        # set relied values
        self.delay = 1000 // self.__framerate   # in ms
        self.dt = float(self.delay) / 1000.0    # in sec
    # end def

    @framerate.deleter
    def framerate (self):
        # delete
        del self.__framerate
    # end def


    @property
    def friction (self):
        """
            attribute property: ground friction to apply to body
            (float, 0.0-1.0, % of velocity);
        """
        return self.__friction
    # end def

    @friction.setter
    def friction (self, value):
        # set value
        self.__friction = min(1.0, abs(float(value)))
    # end def

    @friction.deleter
    def friction (self):
        # delete
        del self.__friction
    # end def


    def start (self, *args, **kw):
        """
            event handler: starts physics computation frames, if not
            already done, does nothing otherwise;
        """
        # allowed to proceed?
        if not self.started:
            # lock flag
            self.started = True
            # release lockers
            self.animations.release(self._computation_loop)
            # start computation frame loop
            self.animations.run_after(
                self.delay, self._computation_loop
            )
        # end if
    # end def


    def stop (self, *args, **kw):
        """
            event handler: stops physics computation frames;
        """
        # lock lockers
        self.animations.lock(self._computation_loop)
        # release flag
        self.started = False
    # end def


    @property
    def update_callback (self):
        """
            attribute property: computation frame update callback for
            owner;
        """
        return self.__update_callback
    # end def

    @update_callback.setter
    def update_callback (self, value):
        # ensure callable
        if callable(value):
            self.__update_callback = value
        else:
            self.__update_callback = lambda *a, **k: None
        # end if
    # end def

    @update_callback.deleter
    def update_callback (self):
        # delete
        del self.__update_callback
    # end def


    def update_closure (self, *args, **kw):
        """
            computation frame callback closure for host updates;
        """
        # enclosed
        def enclosed ():
            self.update_callback(*args, **kw)
        # end def
        return enclosed
    # end def


    @property
    def velocity (self):
        """
            attribute property: body's velocity (Vector2D);
        """
        return self.__velocity
    # end def

    @velocity.setter
    def velocity (self, value):
        # set value
        self.__velocity = Vector2D(value)
    # end def

    @velocity.deleter
    def velocity (self):
        # delete
        del self.__velocity
    # end def

# end class Physics



class Vector2D:
    """
        Generic (x, y) vector for 2D computations;
        This can also be used to represent 2D geometric points;
    """

    def __abs__ (self):
        """
            returns vector magnitude (||v||, float);
        """
        # return magnitude (vector norm)
        return abs(self.as_complex)
    # end def


    def __add__ (self, value):
        """
            addition operator (vector + @value);
            returns new Vector2D as result;
        """
        # ensure vector
        v = Vector2D(value)
        # return result
        return Vector2D(self.x + v.x, self.y + v.y)
    # end def


    def __floordiv__ (self, value):
        """
            floor division operator (vector // @value);
            implemented only for @value as number;
            returns new Vector2D as result;
        """
        # value is a number?
        if isinstance(value, (int, float)):
            # return result
            return Vector2D(self.x // value, self.y // value)
        else:
            # not supported
            return NotImplemented
        # end if
    # end def


    def __init__ (self, x=0, y=0):
        """
            class constructor;
        """
        # x is an ordered iterable?
        if isinstance(x, (tuple, list)):
            # dispatch values
            x, y = x
        # x is maybe a complex number?
        elif isinstance(x, (str, complex)):
            # reset values
            z = complex(str(x).replace(" ", ""))
            x, y = (z.real, z.imag)
        # x is Vector2D?
        elif isinstance(x, Vector2D):
            # copy values
            x, y = (x.x, x.y)
        # end if
        # init members
        self.x, self.y = (x, y)
    # end def


    def __mul__ (self, value):
        """
            multiplication operator (vector * @value);
            returns scalar product (new Vector2D) if @value is a number;
            returns vector cross product (float) if @value is a vector;
        """
        # value is a number?
        if isinstance(value, (int, float)):
            # scalar product
            return Vector2D(self.x * value, self.y * value)
        # value should be a vector
        else:
            # ensure vector
            v = Vector2D(value)
            # return vector cross (float)
            return (self.x * v.x) + (self.y * v.y)
        # end if
    # end def


    def __neg__ (self):
        """
            unary negative operator (-vector);
            returns new Vector2D as result;
        """
        # negate coords
        return Vector2D(-self.x, -self.y)
    # end def


    def __pos__ (self):
        """
            unary positive operator (+vector);
            returns new Vector2D as result;
            returns a copy of current vector, in fact;
        """
        # get copy
        return Vector2D(self.x, self.y)
    # end def


    def __radd__ (self, value):
        """
            reverse addition operator
            (@value + vector --> vector.__radd__(@value));
            returns new Vector2D as result;
        """
        # same as __add__
        return self.__add__(value)
    # end def


    def __rmul__ (self, value):
        """
            reverse multiplication operator
            (@value * vector --> vector.__rmul__(@value));
            returns same results than multiplication operator;
        """
        # same as __mul__
        return self.__mul__(value)
    # end def


    def __rsub__ (self, value):
        """
            reverse substraction operator
            (@value - vector --> vector.__rsub__(@value));
            returns new Vector2D as result;
        """
        # ensure vector
        v = Vector2D(value)
        # return result
        return Vector2D(v.x - self.x, v.y - self.y)
    # end def


    def __str__ (self):
        """
            string representation of class instance (object);
        """
        return "{}{}".format(self.__class__.__name__, self.as_tuple)
    # end def


    def __sub__ (self, value):
        """
            substraction operator (vector - @value);
            returns new Vector2D as result;
        """
        # ensure vector
        v = Vector2D(value)
        # return result
        return Vector2D(self.x - v.x, self.y - v.y)
    # end def


    def __truediv__ (self, value):
        """
            true division operator (vector / @value);
            implemented only for @value as number;
            returns new Vector2D as result;
        """
        # value is a number?
        if isinstance(value, (int, float)):
            # return result
            return Vector2D(self.x / value, self.y / value)
        else:
            # not supported
            return NotImplemented
        # end if
    # end def


    @property
    def as_complex (self):
        """
            attribute property (read-only);
            returns current (x, y) coords converted to complex number;
        """
        return complex(self.x, self.y)
    # end def


    @property
    def as_list (self):
        """
            attribute property (read-only);
            returns current (x, y) coords converted to Python list;
        """
        return [self.x, self.y]
    # end def


    @property
    def as_tuple (self):
        """
            attribute property (read-only);
            returns current (x, y) coords converted to Python tuple;
        """
        return (self.x, self.y)
    # end def


    def ensure_float (self, value, ndigits=9):
        """
            ensures to always return a float value (rounded to
            @ndigits) in any case; returns 0.0 on errors;
        """
        try:
            return round(float(value), ndigits)
        except:
            return 0.0
        # end try
    # end def


    def rotate (self, angle):
        """
            internally rotates vector to absolute @angle (radians);
            returns self pointer;
        """
        # rotate absolute angle
        z = cmath.rect(abs(self), angle)
        # reset coords
        self.x, self.y = (z.real, z.imag)
        # get pointer
        return self
    # end def


    def rotate_rel (self, angle):
        """
            internally rotates vector to relative @angle (radians)
            returns self pointer;
        """
        # rotate relative angle
        r, phi = cmath.polar(self.as_complex)
        z = cmath.rect(r, phi + angle)
        # reset coords
        self.x, self.y = (z.real, z.imag)
        # get pointer
        return self
    # end def


    @property
    def x (self):
        """
            attribute property: coordinate x;
        """
        # get value
        return self.__x
    # end def

    @x.setter
    def x (self, value):
        # set value
        self.__x = self.ensure_float(value)
    # end def

    @x.deleter
    def x (self):
        # delete
        del self.__x
    # end def


    @property
    def y (self):
        """
            attribute property: coordinate y;
        """
        # get value
        return self.__y
    # end def

    @y.setter
    def y (self, value):
        # set value
        self.__y = self.ensure_float(value)
    # end def

    @y.deleter
    def y (self):
        # delete
        del self.__y
    # end def

# end class Vector2D
