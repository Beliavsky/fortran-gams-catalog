! Catalog-owned analytic checks of GAMS E3c using CHEBEXPS.
! Upstream source is downloaded at a pinned revision; it is not bundled here.
program basis
 use iso_fortran_env, only: real64
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer :: n,k,j,count
 real(real64), allocatable :: x(:),weights(:),u(:,:),v(:,:),a(:,:),d(:,:),w(:),ending(:),values(:),want(:),got(:)
 real(real64) :: error,maximum,endpoint
 real(real64), parameter :: tolerance=2.e-11_real64
 external :: chebexps,chebinmt
 maximum=0
 count=0
 do j=1,4
   n=2**j
   allocate(x(n),weights(n),u(n,n),v(n,n),a(n,n),d(n,n),w(3*n*n+2*n+50), &
      ending(n),values(n),want(n),got(n))
   call chebexps(2,n,x,u,v,weights)
   do k=0,n-1
     values=cos(real(k,real64)*acos(x))
     got=matmul(u,values)
     want=0;want(k+1)=1
     call verify()
     got=matmul(v,want)
     want=values
     call verify()
   end do
   deallocate(x,weights,u,v,a,d,w,ending,values,want,got)
 end do
 print '(a,i0)', 'Checked polynomial cases: ',count
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS basis'
contains
 subroutine verify()
   if(.not.all(ieee_is_finite(got))) error stop 'nonfinite result'
   error=maxval(abs(got-want))/max(1._real64,maxval(abs(want)))
   maximum=max(maximum,error)
   if(error>tolerance) error stop 'analytic polynomial mismatch'
   count=count+1
 end subroutine
end program
