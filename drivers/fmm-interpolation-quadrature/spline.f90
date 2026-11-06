! GAMS E1a: checked ForsytheMalcolmMoler spline interface.
program spline
 use ForsytheMalcolmMoler, only: FMMspline,NaturalSpline,Seval,Seval3
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer,parameter :: dp=selected_real_kind(10,50),sizes(*)=[2,3,4,6,9]
 real(dp),parameter :: queries(*)=[-1.2_dp,-1._dp,-.9_dp,-.5_dp,0._dp,.25_dp,.5_dp,1._dp,1.3_dp,1.7_dp,2._dp,2.2_dp,-.3_dp]
 integer :: mode,k,n,degree,i,j,maxdegree,count
 real(dp),allocatable :: x(:),y(:),b(:),c(:),d(:)
 real(dp) :: q,expected(4),got(4),error,maximum
 maximum=0;count=0
 do k=1,size(sizes)
  n=sizes(k)
  allocate(x(n),y(n),b(n),c(n),d(n))
  do i=1,n
   x(i)=-1._dp+3._dp*(real(i-1,dp)/real(n-1,dp))**1.3_dp
  end do
  do mode=1,2
   maxdegree=min(3,n-1)
   if(mode==2) maxdegree=1
   do degree=0,maxdegree
    y=x**degree
    if(mode==1) then
     call FMMspline(x,y,b,c,d)
    else
     call NaturalSpline(x,y,b,c,d)
     if(abs(c(1))+abs(c(n))>5.e-11_dp) error stop 'natural endpoint curvature'
    end if
    do j=1,size(queries)+n
     if(j<=size(queries)) then
      q=queries(j)
     else
      q=x(j-size(queries))
     end if
     expected=0
     expected(1)=q**degree
     if(degree>=1) expected(2)=degree*q**(degree-1)
     if(degree>=2) expected(3)=degree*(degree-1)*q**(degree-2)
     if(degree>=3) expected(4)=degree*(degree-1)*(degree-2)*q**(degree-3)
     got=0;got(1)=Seval(q,x,y,b,c,d)
     expected(2:)=0
     if(.not.all(ieee_is_finite(got))) error stop 'nonfinite spline'
     error=maxval(abs(got-expected))/max(1._dp,maxval(abs(expected)))
     maximum=max(maximum,error)
     if(error>5.e-11_dp) error stop 'spline polynomial mismatch'
     count=count+1
    end do
   end do
  end do
  deallocate(x,y,b,c,d)
 end do
 ! Three-knot non-affine natural spline: exact piecewise cubic, no second solver used.
 allocate(x(3),y(3),b(3),c(3),d(3))
 x=[0._dp,1._dp,2._dp];y=[0._dp,1._dp,0._dp]
 call NaturalSpline(x,y,b,c,d)
 do j=-1,9
  q=0.25_dp*j
  if(q<1._dp) then
   expected=[1.5_dp*q-0.5_dp*q**3,1.5_dp-1.5_dp*q*q,-3._dp*q,-3._dp]
  else
   expected=[1._dp-1.5_dp*(q-1)**2+0.5_dp*(q-1)**3,-3._dp*(q-1)+1.5_dp*(q-1)**2, &
     -3._dp+3._dp*(q-1),3._dp]
  end if
 got=0;got(1)=Seval(q,x,y,b,c,d);expected(2:)=0
  if(.not.all(ieee_is_finite(got))) error stop 'nonfinite natural spline'
  error=maxval(abs(got-expected))/max(1._dp,maxval(abs(expected)))
  maximum=max(maximum,error)
  if(error>5.e-11_dp) error stop 'natural spline reference mismatch'
  count=count+1
 end do
 deallocate(x,y,b,c,d)
 print '(a,i0)', 'Checked spline queries: ',count
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS spline'
end program
